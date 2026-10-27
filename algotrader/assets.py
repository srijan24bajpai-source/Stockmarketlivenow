"""Instrument universe: India (NSE+BSE equities, indices, futures, options), US, crypto."""

IN_NSE = """
RELIANCE|Reliance Industries|Energy;TCS|Tata Consultancy Services|IT;HDFCBANK|HDFC Bank|Banking
INFY|Infosys|IT;ICICIBANK|ICICI Bank|Banking;HINDUNILVR|Hindustan Unilever|FMCG;ITC|ITC|FMCG
SBIN|State Bank of India|Banking;BHARTIARTL|Bharti Airtel|Telecom;KOTAKBANK|Kotak Mahindra Bank|Banking
LT|Larsen & Toubro|Infra;AXISBANK|Axis Bank|Banking;BAJFINANCE|Bajaj Finance|NBFC
ASIANPAINT|Asian Paints|FMCG;MARUTI|Maruti Suzuki|Auto;SUNPHARMA|Sun Pharma|Pharma;TITAN|Titan|Consumer
WIPRO|Wipro|IT;HCLTECH|HCL Technologies|IT;NTPC|NTPC|Power;ONGC|ONGC|Energy;TATAMOTORS|Tata Motors|Auto
TATASTEEL|Tata Steel|Metals;ADANIENT|Adani Enterprises|Conglomerate;ZOMATO|Eternal (Zomato)|Consumer
POWERGRID|Power Grid|Power;ADANIPORTS|Adani Ports|Infra;COALINDIA|Coal India|Mining;BPCL|BPCL|Energy
IOC|Indian Oil|Energy;GAIL|GAIL|Energy;DLF|DLF|Realty;JSWSTEEL|JSW Steel|Metals;GRASIM|Grasim|Cement
CIPLA|Cipla|Pharma;DRREDDY|Dr Reddy's|Pharma;DIVISLAB|Divi's Labs|Pharma;EICHERMOT|Eicher Motors|Auto
HEROMOTOCO|Hero MotoCorp|Auto;BAJAJ-AUTO|Bajaj Auto|Auto;M&M|Mahindra & Mahindra|Auto
TATAPOWER|Tata Power|Power;TECHM|Tech Mahindra|IT;ULTRACEMCO|UltraTech Cement|Cement;VEDL|Vedanta|Metals
HAL|Hindustan Aeronautics|Defence;IRCTC|IRCTC|Travel;PNB|Punjab National Bank|Banking
CANBK|Canara Bank|Banking;BANKBARODA|Bank of Baroda|Banking;INDUSINDBK|IndusInd Bank|Banking
SBILIFE|SBI Life|Insurance;HDFCLIFE|HDFC Life|Insurance;PIDILITIND|Pidilite|Chemicals
DABUR|Dabur|FMCG;BRITANNIA|Britannia|FMCG;NESTLEIND|Nestle India|FMCG;HAVELLS|Havells|Consumer
SIEMENS|Siemens India|Capital Goods;BEL|Bharat Electronics|Defence;YESBANK|Yes Bank|Banking
IDFCFIRSTB|IDFC First Bank|Banking;TATACONSUM|Tata Consumer|FMCG;SHRIRAMFIN|Shriram Finance|NBFC
"""
IN_BSE = """
500325|Reliance Industries (BSE)|Energy;532540|TCS (BSE)|IT;500180|HDFC Bank (BSE)|Banking
500209|Infosys (BSE)|IT;532174|ICICI Bank (BSE)|Banking;500875|ITC (BSE)|FMCG
500112|State Bank of India (BSE)|Banking;532454|Bharti Airtel (BSE)|Telecom
500247|Kotak Mahindra Bank (BSE)|Banking;500510|Larsen & Toubro (BSE)|Infra
532215|Axis Bank (BSE)|Banking;500034|Bajaj Finance (BSE)|NBFC
500820|Asian Paints (BSE)|FMCG;532500|Maruti Suzuki (BSE)|Auto;500124|Dr Reddy's (BSE)|Pharma
"""
INDICES = [("^NSEI", "NIFTY 50", "Index"), ("^NSEBANK", "BANK NIFTY", "Index"),
           ("^BSESN", "SENSEX", "Index"), ("^INDIAVIX", "India VIX", "Index")]
CRYPTO = [("BTC-USD", "Bitcoin"), ("ETH-USD", "Ethereum"), ("SOL-USD", "Solana"),
          ("XRP-USD", "XRP"), ("DOGE-USD", "Dogecoin")]
# (id, name, yahoo, lot, underlying)
FUTURES = [("NIFTY-FUT", "NIFTY 50 Futures", "^NSEI", 75), ("BANKNIFTY-FUT", "Bank Nifty Futures", "^NSEBANK", 15),
           ("SENSEX-FUT", "Sensex Futures", "^BSESN", 10), ("RELIANCE-FUT", "Reliance Futures", "RELIANCE", 250),
           ("HDFCBANK-FUT", "HDFC Bank Futures", "HDFCBANK", 550), ("TCS-FUT", "TCS Futures", "TCS", 175)]
OPT_UND = [("NIFTY", "^NSEI", 75), ("BANKNIFTY", "^NSEBANK", 15), ("SENSEX", "^BSESN", 10)]
US = """
AAPL|Apple|Technology;MSFT|Microsoft|Technology;NVDA|NVIDIA|Technology;GOOGL|Alphabet|Communication
AMZN|Amazon|Consumer;META|Meta Platforms|Communication;TSLA|Tesla|Consumer;AVGO|Broadcom|Technology
ORCL|Oracle|Technology;ADBE|Adobe|Technology;AMD|AMD|Technology;NFLX|Netflix|Communication
DIS|Disney|Communication;JPM|JPMorgan Chase|Financials;GS|Goldman Sachs|Financials;V|Visa|Financials
MA|Mastercard|Financials;UNH|UnitedHealth|Healthcare;LLY|Eli Lilly|Healthcare;JNJ|Johnson & Johnson|Healthcare
WMT|Walmart|Consumer;COST|Costco|Consumer;HD|Home Depot|Consumer;NKE|Nike|Consumer;MCD|McDonald's|Consumer
KO|Coca-Cola|Consumer;PEP|PepsiCo|Consumer;PG|Procter & Gamble|Consumer;XOM|Exxon Mobil|Energy
CVX|Chevron|Energy;BA|Boeing|Industrials;CAT|Caterpillar|Industrials;GE|GE Aerospace|Industrials
PLTR|Palantir|Technology;COIN|Coinbase|Financials;UBER|Uber|Technology;SHOP|Shopify|Technology
"""


def _rows(blob, **fixed):
    out = []
    for line in blob.replace("\n", ";").split(";"):
        line = line.strip()
        if not line:
            continue
        sym, name, sec = line.split("|")
        out.append(dict(symbol=sym, name=name, sector=sec, **fixed))
    return out


def _equities(rows, market, yahoo_suffix):
    for r in rows:
        r["market"] = market
        r["type"] = "STOCK"
        r["yahoo"] = r["symbol"] + yahoo_suffix
        r["unit"] = 1
        r["margin"] = 1.0
        r["currency"] = "INR" if market == "IN" else "USD"
    return rows


INSTRUMENTS = []
INSTRUMENTS += _equities(_rows(IN_NSE, exchange="NSE"), "IN", ".NS")
INSTRUMENTS += _equities(_rows(IN_BSE, exchange="BSE"), "IN", ".BO")
for sym, name, sec in INDICES:
    INSTRUMENTS.append(dict(symbol=sym, name=name, sector=sec, market="IN", exchange="NSE",
                            type="INDEX", yahoo=sym, unit=1, margin=1.0, currency="INR"))
for fid, name, und, lot in FUTURES:
    INSTRUMENTS.append(dict(symbol=fid, name=name, sector="Futures", market="IN", exchange="F&O",
                            type="FUT", yahoo=(und if und.startswith("^") else und + ".NS"),
                            unit=lot, margin=0.12, currency="INR"))
for sym, name in CRYPTO:
    INSTRUMENTS.append(dict(symbol=sym, name=name, sector="Crypto", market="CRYPTO", exchange="Crypto",
                            type="CRYPTO", yahoo=sym, unit=1, margin=1.0, currency="USD"))
INSTRUMENTS += _equities(_rows(US, exchange="US"), "US", "")
for i in INSTRUMENTS:
    if i["market"] == "US":
        i["yahoo"] = i["symbol"].replace(".", "-")

BY_ID = {i["symbol"]: i for i in INSTRUMENTS}
OPT_UNDERLYINGS = {u: (y, l) for u, y, l in OPT_UND}
META = {s: {"symbol": s, "name": i["name"], "sector": i["sector"], "exchange": i["exchange"],
            "market": i["market"], "type": i["type"]} for s, i in BY_ID.items()}
