import logging
from typing import List

import requests
from retry import retry
import pandas as pd

BASE_URL = "https://deribit.com/api/v2"
CRYPTOS = ['BTC', 'ETH']

logging.basicConfig(
    format="%(asctime)s:%(levelname)s: - %(message)s",
    level=logging.INFO,
)

@retry(tries=2, delay=5)
def get_option_instruments(currency: str) -> List[dict]:

    logging.info(f'Getting {currency} option instruments')
    
    END_POINT = '/public/get_instruments'
    parameters = f'?currency={currency}&expired=false&kind=option'
    url = BASE_URL + END_POINT + parameters
    r = requests.get(url)
    r.raise_for_status()

    return r.json()["result"]

@retry(tries=2, delay=5)
def get_tick_data(instrument: str) -> List[dict]:

    logging.info(f'Getting tick data for {instrument}')

    END_POINT = '/public/ticker'
    parameters = f'?instrument_name={instrument}'
    url = BASE_URL + END_POINT + parameters
    r = requests.get(url)
    r.raise_for_status()

    return r.json()["result"]

def combine_data(instruments: List[dict], tick_data: List[dict]) -> pd.DataFrame:

    logging.info(f'Combining the data sets')

    inst_df = pd.DataFrame(instruments)
    inst_df.set_index("instrument_name", inplace=True)
    tick_df = pd.json_normalize(tick_data)
    tick_df.set_index("instrument_name", inplace=True)

    result_df = inst_df.join(tick_df)

    return result_df

def get_market_data(currency: str) -> None:

    logging.info(f'Getting market data for {currency} options')

    instruments = get_option_instruments(currency)

    raw_options_data = []
    for instrument in instruments:
        name = instrument["instrument_name"]
        raw_options_data.append(get_tick_data(name))

    options_data = combine_data(instruments, raw_options_data)

    options_data.to_csv(f'data_{currency}.csv')

if __name__ == "__main__":
    
    for crypto in CRYPTOS:
        get_market_data(crypto)
