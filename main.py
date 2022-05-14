import sys
import requests
import json

BARS = "=" * 65

# base API call e.g: f(price, {ids: bitcoin, vs_currencies: usd})
def coingecko_api_call(endpoint: str, params: dict) -> dict:
    url: str = "https://api.coingecko.com/api/v3/" + endpoint 
    return json.loads(requests.get(url=url, params=params).text)

# hits /coins/{id}; returns a big ole json thing
def base_info(coin_id: str) -> dict:
    return coingecko_api_call(f"coins/{coin_id}", {})

# the thing
def print_info(coin_id):
    denom = "usd"
    raw = base_info(coin_id)
    outstr = f"{raw.get('id')} / ${raw.get('symbol').upper()}" + "\n" + f"{BARS}" + "\n"
    outstr += f"website: {raw.get('links').get('homepage')[0]}"+"\n"+"addresses:\n"
    addrs = raw.get("platforms")
    fake_ass_chains = ["tomochain"]
    for k, v in addrs.items():
        if len(k) > 1 and len(v) > 1 and k not in fake_ass_chains:
            outstr += f"\t{k}: {v}\n"
    mktdata = raw.get('market_data')
    outstr += f"{BARS}\n\tprice: {round(mktdata.get('current_price').get(denom),5):,}\t\t\t"
    outstr += f"mcap: {mktdata.get('market_cap').get(denom):,}"+"\n\t"
    outstr += f"24h: {round(mktdata.get('price_change_percentage_24h'), 2)}%"+"\t\t\t"
    outstr += f"FDV: {mktdata.get('fully_diluted_valuation').get(denom):,}\n\t"
    outstr += f"7d: {round(mktdata.get('price_change_percentage_7d'), 2)}%"+"\t\t\t"
    outstr += f"volume: {mktdata.get('total_volume').get(denom):,}"+"\n\t"
    outstr += f"60d: {round(mktdata.get('price_change_percentage_60d'), 2)}%"+"\t\t\t"
    outstr += f"ath: {mktdata.get('ath').get(denom):,}"+"\n"+BARS
    print(outstr)


def main(arg):
    print_info(arg)

if __name__ == "__main__":
    main(sys.argv[1])



