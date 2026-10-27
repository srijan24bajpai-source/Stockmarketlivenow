"""Live data for every instrument type. Yahoo Finance public endpoint, with a simulated fallback."""
import json
import math
import time
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor

from . import options as opt
from .assets import BY_ID, INSTRUMENTS, LOTS, OPT_UNDERLYINGS

ID_PREFIX = {"^NSEI": "NIFTY", "^NSEBANK": "BANKNIFTY", "^BSESN": "SENSEX"}
PREFIX_TO_SYMBOL = {v: k for k, v in ID_PREFIX.items()}


def id_prefix(sym):
    return ID_PREFIX.get(sym, sym)
from .data import generate_prices

_cache = {}
UA = {"User-Agent": "Mozilla/5.0"}


def _get(url, ttl=0, key=None):
    if key and key in _cache:
        ts, val = _cache[key]
        if time.time() - ts < ttl:
            return val
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=8) as r:
        val = json.load(r)
    if key:
        _cache[key] = (time.time(), val)
    return val


def _chart(symbol, rng="1y", interval="1d", ttl=120):
    url = ("https://query1.finance.yahoo.com/v8/finance/chart/"
           + urllib.parse.quote(symbol, safe="") + "?range=%s&interval=%s" % (rng, interval))
    try:
        res = _get(url, ttl, key=("c", symbol, rng, interval))["chart"]["result"][0]
        rows = [(t, c) for t, c in zip(res["timestamp"], res["indicators"]["quote"][0]["close"]) if c]
        return {"yahoo": symbol, "simulated": False, "currency": res["meta"].get("currency", "USD"),
                "times": [r[0] for r in rows], "closes": [round(r[1], 2) for r in rows],
                "price": round(res["meta"].get("regularMarketPrice") or rows[-1][1], 2)}
    except Exception:
        closes = generate_prices(symbol, 250)
        now = int(time.time())
        return {"yahoo": symbol, "simulated": True, "currency": "USD",
                "times": [now - 86400 * (len(closes) - i) for i in range(len(closes))],
                "closes": closes, "price": closes[-1]}


def usdinr():
    key = ("fx", "usdinr")
    if key in _cache and time.time() - _cache[key][0] < 300:
        return _cache[key][1]
    rate = 83.5
    try:
        r = _get("https://query1.finance.yahoo.com/v8/finance/chart/INR=X?range=1d&interval=1d")
        rate = round(r["chart"]["result"][0]["meta"]["regularMarketPrice"], 2)
    except Exception:
        pass
    _cache[key] = (time.time(), rate)
    return rate


def _expiry_days():
    now = time.gmtime()
    days = (3 - now.tm_wday) % 7  # next Thursday (2026-10-27 is a Tuesday)
    return days if days else 7


def option_list():
    """Build the option chain instruments from live spot + realised vol."""
    out = []
    with ThreadPoolExecutor(max_workers=3) as ex:
        spots = list(ex.map(lambda u: (_chart(u[1][0], ttl=30)["closes"], _chart(u[1][0], ttl=30)["price"]), OPT_UNDERLYINGS.items()))
    for (name, (y, lot)), (closes, spot) in zip(OPT_UNDERLYINGS.items(), spots):
        sigma = opt.realized_vol(closes)
        for row in opt.chain(name, spot, _expiry_days(), sigma, strikes=5):
            out.append(dict(symbol=row["symbol"], name="%s %d %s" % (name, row["strike"], row["side"]),
                            sector="Options", market="IN", exchange="F&O", type="OPT",
                            yahoo=y, unit=lot, margin=1.0, currency="INR", strike=row["strike"],
                            side=row["side"], underlying=name, expiry_days=_expiry_days(),
                            price=row["price"], sigma=round(sigma, 3)))
    return out


def instruments(market=None):
    rows = [dict(i) for i in INSTRUMENTS]
    rows += option_list()
    if market:
        rows = [r for r in rows if r["market"] == market]
    return rows


def by_id(sid):
    i = BY_ID.get(sid)
    if i:
        return i
    for o in option_list():
        if o["symbol"] == sid:
            return o
    return option_instrument(sid)


def name_of(sid):
    try:
        return by_id(sid)["name"]
    except KeyError:
        return sid


def price_of(sid):
    i = by_id(sid)
    if i["type"] == "OPT":
        spot = _chart(i["yahoo"], ttl=30)["price"]
        return round(opt.bs(spot, i["strike"], i["expiry_days"] / 365, i["sigma"], i["side"] == "CE"), 2)
    return _chart(i["yahoo"], ttl=30)["price"]


def quote(sid):
    i = by_id(sid)
    h = _chart(i["yahoo"], rng="5d", ttl=8)
    if i["type"] == "OPT":
        px = price_of(sid)
        return {"symbol": sid, "price": px, "change_pct": 0.0, "currency": "INR",
                "simulated": h["simulated"], "type": "OPT"}
    prev = h["closes"][-2] if len(h["closes"]) > 1 else h["price"]
    chg = (h["price"] / prev - 1) * 100 if prev else 0
    return {"symbol": sid, "price": h["price"], "change_pct": round(chg, 2),
            "currency": i["currency"], "simulated": h["simulated"], "type": i["type"]}


def quotes(ids):
    ids = [s for s in ids if s][:30]
    def safe(s):
        try:
            return quote(s)
        except Exception:
            return None
    with ThreadPoolExecutor(max_workers=10) as ex:
        return [q for q in ex.map(safe, ids) if q]


def history(sid):
    i = by_id(sid)
    h = _chart(i["yahoo"], ttl=120)
    h = dict(h)
    h["symbol"] = sid
    h["currency"] = i["currency"]
    h["type"] = i["type"]
    if i["type"] == "OPT":
        h["price"] = price_of(sid)
        h["label"] = i["underlying"] + " spot (option priced by Black-Scholes)"
    return h


def _last_thursday_days():
    """Days to the last Thursday of this month (stock F&O monthly expiry)."""
    now = time.gmtime()
    y, m = now.tm_year, now.tm_mon
    nxt = time.gmtime(time.mktime((y + (m == 12), (m % 12) + 1, 1, 0, 0, 0, 0, 0, 0)))
    last_day = time.mktime(nxt) - 86400
    lt = time.gmtime(last_day)
    while lt.tm_wday != 3:
        last_day -= 86400
        lt = time.gmtime(last_day)
    today = time.mktime(time.gmtime()[:3] + (0, 0, 0, 0, 0, 0))
    days = int((last_day - today) / 86400)
    if days < 1:
        days += 28
    return days


STRIKE_STEP = {"NIFTY": 50, "BANKNIFTY": 100, "SENSEX": 100}


def _strike_step(spot, prefix=""):
    if prefix in STRIKE_STEP:
        return STRIKE_STEP[prefix]
    if spot > 5000:
        return 100
    if spot > 2500:
        return 50
    if spot > 1000:
        return 20
    if spot > 500:
        return 10
    if spot > 200:
        return 5
    return 2.5


def _last_weekday_days(wd, is_index):
    """Days to the last Tue (indices) / Thu (stocks) of this month; rolls to next month if past."""
    now = time.gmtime()
    y, m = now.tm_year, now.tm_mon
    for add in (0, 1):
        mm = m + add
        yy = y + (mm - 1) // 12
        mm = (mm - 1) % 12 + 1
        first_next = time.mktime((yy + (mm == 12), (mm % 12) + 1, 1, 0, 0, 0, 0, 0, 0))
        last = time.gmtime(first_next - 86400)
        while last.tm_wday != wd:
            first_next -= 86400
            last = time.gmtime(first_next - 86400)
        days = int((time.mktime(last[:3] + (0, 0, 0, 0, 0, 0)) + 86399 - time.time()) / 86400) + 1
        if days >= 1:
            return days
    return 28


def expiry_days(prefix, is_index, kind="weekly"):
    if kind == "today":
        return 0
    if kind == "1d":
        return 1
    if kind == "monthly":
        return _last_weekday_days(1 if is_index else 3, is_index)
    wd = 3 if prefix == "SENSEX" else 1
    d = (wd - time.gmtime().tm_wday) % 7
    return d if d > 0 else 7


def option_chain(underlying, strikes=8, target=None, expiry="weekly", extra=()):
    """Chain for an index or any NIFTY 50 stock: 50-pt NIFTY ladder, smile-priced, any strike on request."""
    i = BY_ID.get(underlying.upper())
    if not i:
        raise KeyError(underlying)
    h = _chart(i["yahoo"], ttl=30)
    spot = h["price"]
    prefix = id_prefix(i["symbol"])
    lot = LOTS.get(prefix, 1 if i["type"] == "INDEX" else 500)
    days = expiry_days(prefix, i["type"] == "INDEX", expiry or "weekly")
    atm_iv = opt.atm_iv_from_realised(opt.realized_vol(h["closes"]))
    step = _strike_step(spot, prefix)
    atm = int(round(spot / step) * step)
    ks = {atm + k * step for k in range(-strikes, strikes + 1)}
    for x in extra:
        try:
            ks.add(float(x))
        except (TypeError, ValueError):
            continue
    T = max(days, 0.5) / 365
    rows = []
    for K in sorted(ks, reverse=True):
        m = K / spot - 1
        row = {"strike": K if float(K).is_integer() else K, "atm": abs(K - atm) < 1e-9,
               "moneyness": round(m * 100, 2), "ce": {}, "pe": {}}
        for side, call in (("ce", True), ("pe", False)):
            iv = opt.smile_iv(atm_iv, m, "CE" if call else "PE")
            px = round(opt.bs(spot, K, T, iv, call), 2)
            d1 = (math.log(spot / K) + (0.065 + iv ** 2 / 2) * T) / (iv * math.sqrt(T))
            row[side] = {"id": "%s-%s-%s" % (prefix, ("%d" % K) if float(K).is_integer() else K,
                                                "CE" if call else "PE"),
                         "price": px, "delta": round(_nd(d1) if call else _nd(d1) - 1, 2),
                         "iv": round(iv * 100, 1), "contract": round(px * lot, 2)}
        rows.append(row)
    near = None
    if target:
        cand = [{"strike": K, "side": s.upper(), "price": row[s]["price"], "id": row[s]["id"]}
                for row in rows for K, s in ((row["strike"], "ce"), (row["strike"], "pe"))]
        if cand:
            near = min(cand, key=lambda c: abs(c["price"] - float(target)))
    return {"underlying": i["symbol"], "id_prefix": prefix, "name": i["name"], "spot": spot,
            "lot": lot, "expiry_days": days, "expiry_kind": expiry, "atm_iv": round(atm_iv * 100, 1),
            "atm": atm, "step": step, "strikes": rows, "near_target": near,
            "simulated": h["simulated"], "currency": "INR"}


def _nd(x):
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))


def option_instrument(oid):
    """Resolve 'RELIANCE-1400-CE' style ids into a tradeable instrument."""
    import re
    m = re.match(r"^(.+)-(\d+)-(CE|PE)$", oid.upper())
    if not m:
        raise KeyError(oid)
    und, strike, side = m.group(1), int(m.group(2)), m.group(3)
    sym = PREFIX_TO_SYMBOL.get(und, und)
    base = BY_ID.get(sym)
    if not base:
        raise KeyError(oid)
    h = _chart(base["yahoo"], ttl=30)
    atm_iv = opt.atm_iv_from_realised(opt.realized_vol(h["closes"]))
    sigma = opt.smile_iv(atm_iv, strike / h["price"] - 1, side)
    pref = id_prefix(base["symbol"])
    days = expiry_days(pref, base["type"] == "INDEX", "weekly")
    lot = LOTS.get(und, LOTS.get(sym, 1 if base["type"] == "INDEX" else 500))
    return {"symbol": oid.upper(), "name": "%s %d %s" % (und, strike, side), "sector": "Options",
            "market": "IN", "exchange": "F&O", "type": "OPT", "yahoo": base["yahoo"],
            "unit": lot, "margin": 1.0, "currency": "INR", "strike": strike, "side": side,
            "underlying": und, "expiry_days": days, "sigma": round(sigma, 3),
            "price": round(opt.bs(h["price"], strike, days / 365, sigma, side == "CE"), 2)}
