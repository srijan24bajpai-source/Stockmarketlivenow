"""Live data for every instrument type. Yahoo Finance public endpoint, with a simulated fallback."""
import json
import math
import time
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor

from . import options as opt
from .assets import BY_ID, INSTRUMENTS, OPT_UNDERLYINGS
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
    raise KeyError(sid)


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
