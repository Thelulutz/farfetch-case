import pandas as pd
import requests
import io


pd.set_option('mode.chained_assignment', None)
#### Getting the exchange rate from EUR to USD in 2023-03-01 (YYYY-MM-DD)
entrypoint_exr = 'https://sdw-wsrest.ecb.europa.eu/service/'
resource_exr = 'data'                       # 'data' is used for data queries
flowRef_exr = 'EXR'                         # describes that needs to be returned, exchange rates for this one
keyFreq_exr = 'D'                           # describes the frequency of the measurement, D is for daily
keyCurr_exr = 'USD'                         # the currency being measured
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
    'startPeriod': '2023-03-01',    # Start date
    'endPeriod': '2023-03-01'       # End date
}

url_exr = entrypoint_exr + resource_exr + '/' + flowRef_exr + '/' + url_keys
response_exr = requests.get(url_exr, params=parameters, headers={'Accept': 'text/csv'})
df = pd.read_csv(io.StringIO(response_exr.text))
exchange_rate = df.iloc[0].OBS_VALUE    # This value will be used to make the conversion from USD to EUR

#### Getting all shoe products
url_categories = 'https://api.escuelajs.co/api/v1/categories?limit=100'
response_categories = requests.get(url_categories)
# For getting the id of the category Shoes, this loop was used
for i in response_categories.json():
    if i['name'] == 'Shoes':
        categoryId = i['id']
        break

url_shoes = f'https://api.escuelajs.co/api/v1/products/?categoryId={categoryId}'
response_shoes = requests.get(url_shoes)
df_response = pd.DataFrame(response_shoes.json())
df_shoes = df_response[['title', 'description', 'price']]
df_shoes.columns = ['Title', 'Description', 'Price_USD']    # Columns selected and renamed
df_shoes['Price_EUR'] = df_shoes['Price_USD'].apply(lambda x: round(x/exchange_rate, 2))    # Conversion applied on the value and created a new column for it
df_shoes = df_shoes.assign(Date_ExchangeRate='2023-03-01')  # Date used for the exchange rate
df_shoes.to_csv('shoes_prices.csv', index=False)
