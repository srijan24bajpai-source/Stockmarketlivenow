"""Instrument universe: India (NSE+BSE equities, indices, futures, options), US, crypto."""

IN_NSE = """
RELIANCE|Reliance Industries|Energy;HDFCBANK|HDFC Bank|Banking;ICICIBANK|ICICI Bank|Banking;INFY|Infosys|IT
TCS|Tata Consultancy Services|IT;BHARTIARTL|Bharti Airtel|Telecom;ITC|ITC|FMCG;SBIN|State Bank of India|Banking
LT|Larsen & Toubro|Infra;KOTAKBANK|Kotak Mahindra Bank|Banking;HINDUNILVR|Hindustan Unilever|FMCG;AXISBANK|Axis Bank|Banking
BAJFINANCE|Bajaj Finance|NBFC;MARUTI|Maruti Suzuki|Auto;M&M|Mahindra & Mahindra|Auto;SUNPHARMA|Sun Pharma|Pharma
ULTRACEMCO|UltraTech Cement|Cement;TITAN|Titan|Consumer;NTPC|NTPC|Power;POWERGRID|Power Grid|Power
TATAMOTORS|Tata Motors|Auto;TATASTEEL|Tata Steel|Metals;JSWSTEEL|JSW Steel|Metals;ADANIENT|Adani Enterprises|Conglomerate
ADANIPORTS|Adani Ports|Infra;COALINDIA|Coal India|Mining;ONGC|ONGC|Energy;BPCL|BPCL|Energy;GRASIM|Grasim|Cement
HINDALCO|Hindalco|Metals;DRREDDY|Dr Reddy's|Pharma;CIPLA|Cipla|Pharma;APOLLOHOSP|Apollo Hospitals|Healthcare
BAJAJFINSV|Bajaj Finserv|NBFC;BAJAJ-AUTO|Bajaj Auto|Auto;EICHERMOT|Eicher Motors|Auto;HEROMOTOCO|Hero MotoCorp|Auto
BRITANNIA|Britannia|FMCG;NESTLEIND|Nestle India|FMCG;TATACONSUM|Tata Consumer|FMCG;SBILIFE|SBI Life|Insurance
HDFCLIFE|HDFC Life|Insurance;TECHM|Tech Mahindra|IT;WIPRO|Wipro|IT;ASIANPAINT|Asian Paints|FMCG
TRENT|Trent|Retail;INDUSINDBK|IndusInd Bank|Banking;SHRIRAMFIN|Shriram Finance|NBFC;ETERNAL|Eternal (Zomato)|Consumer
HCLTECH|HCL Technologies|IT
"""
IN_NSE_EXTRA = """
HAL|Hindustan Aeronautics|Defence;BEL|Bharat Electronics|Defence;IRCTC|IRCTC|Travel;PNB|Punjab National Bank|Banking
CANBK|Canara Bank|Banking;BANKBARODA|Bank of Baroda|Banking;DLF|DLF|Realty;VEDL|Vedanta|Metals;GAIL|GAIL|Energy
IOC|Indian Oil|Energy;TATAPOWER|Tata Power|Power;PIDILITIND|Pidilite|Chemicals;DABUR|Dabur|FMCG
HAVELLS|Havells|Consumer;SIEMENS|Siemens India|Capital Goods;YESBANK|Yes Bank|Banking;IDFCFIRSTB|IDFC First Bank|Banking
ZOMATO|Zomato (old symbol)|Consumer;DIVISLAB|Divi's Labs|Pharma;JUBLFOOD|Jubilant FoodWorks|Consumer;POLYCAB|Polycab|Capital Goods
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
NIFTY50 = _rows(IN_NSE, exchange="NSE")
for r in NIFTY50:
    r["nifty50"] = True
INSTRUMENTS += _equities(NIFTY50, "IN", ".NS")
INSTRUMENTS += _equities(_rows(IN_NSE_EXTRA, exchange="NSE", nifty50=False), "IN", ".NS")
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
# approximate F&O lot sizes (contracts are simulated)
LOTS = {"NIFTY": 75, "BANKNIFTY": 15, "SENSEX": 10,
        "RELIANCE": 500, "HDFCBANK": 550, "ICICIBANK": 700, "INFY": 400, "TCS": 175,
        "SBIN": 750, "BHARTIARTL": 475, "ITC": 1600, "LT": 150, "KOTAKBANK": 400,
        "HINDUNILVR": 300, "AXISBANK": 625, "BAJFINANCE": 125, "MARUTI": 50, "M&M": 350,
        "SUNPHARMA": 350, "ULTRACEMCO": 50, "TITAN": 175, "NTPC": 1500, "POWERGRID": 1900,
        "TATAMOTORS": 800, "TATASTEEL": 5500, "JSWSTEEL": 675, "ADANIENT": 300,
        "ADANIPORTS": 475, "COALINDIA": 1350, "ONGC": 2250, "BPCL": 1800, "GRASIM": 250,
        "HINDALCO": 1075, "DRREDDY": 625, "CIPLA": 375, "APOLLOHOSP": 125, "BAJAJFINSV": 500,
        "BAJAJ-AUTO": 75, "EICHERMOT": 175, "HEROMOTOCO": 300, "BRITANNIA": 200, "NESTLEIND": 250,
        "TATACONSUM": 550, "SBILIFE": 375, "HDFCLIFE": 1100, "TECHM": 600, "WIPRO": 3000,
        "ASIANPAINT": 200, "TRENT": 100, "INDUSINDBK": 500, "SHRIRAMFIN": 300, "ETERNAL": 2425,
        "DIVISLAB": 100, "HCLTECH": 350}


META = {s: {"symbol": s, "name": i["name"], "sector": i["sector"], "exchange": i["exchange"],
            "market": i["market"], "type": i["type"]} for s, i in BY_ID.items()}
