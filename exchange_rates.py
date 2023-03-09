import pandas as pd
import requests
import io


#### Declaring variables
list_currencies = [
    'AUD', # Australian Dollar
    'BGN', # Bulgarian Lev
    'BRL', # Brazilian Real
    'CAD', # Canadian Dollar
    'CHF', # Swiss franc
    'CNY', # Chinese Yuan Renminbi
    'CYP', # Chinese Yuan Renminbi
    'CZK', # Czech Koruna
    'DKK', # Danish Krone
    'EEK', # Danish Krone
    'GBP', # Pound Sterling
    'HKD', # Hong Kong Dollar
    'HRK', # Croatian Kuna
    'HUF', # Hungarian Forint
    'IDR', # Indonesian Rupiah
    'ILS', # Israeli Sheqel
    'INR', # Indian Rupee
    'ISK', # Icelandic Krona
    'JPY', # Japanese Yen
    'KRW', # South Korean Won
    'LTL', # South Korean Won
    'LVL', # South Korean Won
    'MTL', # South Korean Won
    'MXN', # Mexican Peso
    'MYR', # Malaysian Ringgit
    'NOK', # Norwegian Krone
    'NZD', # New Zealand Dollar
    'PHP', # Philippine Peso
    'PLN', # Polish Zloty
    'RON', # Romanian Leu
    'RUB', # Russian Ruble
    'SEK', # Swedish Krona
    'SGD', # Singapore Dollar
    'SIT', # Singapore Dollar
    'SKK', # Singapore Dollar
    'THB', # Thai Baht
    'TRL', # Thai Baht
    'TRY', # Turkish Lira
    'USD', # United States Dollar
    'ZAR'  # South African Rand
]
entrypoint_exr = 'https://sdw-wsrest.ecb.europa.eu/service/'
resource_exr = 'data'                       # 'data' is used for data queries
flowRef_exr = 'EXR'                         # describes that needs to be returned, exchange rates for this one
keyFreq_exr = 'D'                           # describes the frequency of the measurement, D is for daily
keyCurr_exr = '+'.join(list_currencies)     # brings the list of currencies being measured
keyEuro_exr = 'EUR'                         # the currency being measured against
type_exr = 'SP00'                           # foreign exchange reference rates have code SP00
seriesVariation_exr = 'A'                   # Average variation for given frequency

keys_list = [
    ('freq', keyFreq_exr),
    ('currency_measured', keyCurr_exr),
    ('currency_against', keyEuro_exr),
    ('type_exchange_rate', type_exr),
    ('series_variation', seriesVariation_exr)
]
url_keys = '.'.join(value for key, value in keys_list)

parameters = {
    'startPeriod': '2023-02-09',    # Start date
    'endPeriod': '2023-02-10'       # End date
}

#### Creating request
url_request = entrypoint_exr + resource_exr + '/' + flowRef_exr + '/' + url_keys
response = requests.get(url_request, params=parameters, headers={'Accept': 'text/csv'})

#### Putting the data into a dataframe and saving it
df = pd.read_csv(io.StringIO(response.text))
df_exr = df[['CURRENCY_DENOM', 'CURRENCY', 'TIME_PERIOD', 'OBS_VALUE', 'TITLE_COMPL']]
df_exr.columns = ['Currency_base', 'Currency_dest', 'Date', 'Exchange_Rate', 'Description']
df_exr.to_csv('exchange_rates_daily.csv', index=False)
