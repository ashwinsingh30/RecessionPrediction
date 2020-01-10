import datetime

import numpy as np
import pandas as pd
from dateutil.relativedelta import relativedelta


def parseDate(date):
    return datetime.datetime.strptime(date, '%Y-%m-%d').date()


def get_fred_data_as_df(combined_data, series_name, file_name):
    path = '/Users/ashwin/PycharmProjects/ResearchPaper/RawData/NovemberData/' + file_name
    print(pd.read_csv(path))
    data = pd.read_csv(path)[['Date', 'Price']]
    # data.Date = data.Date.apply(parseDate)
    data['Series'] = series_name
    return combined_data.append(data, ignore_index=True, sort=False)


def parse_icom_date(date):
    date = date.replace(",", "").replace(" ", "").upper()
    return str(datetime.datetime.strptime(date, "%b%d%Y").date())


def parse_float(value):
    value = value.replace(',','')
    return float(value)


combined_data = pd.DataFrame()

# sp500 = pd.read_csv('/Users/ashwin/PycharmProjects/ResearchPaper/RawData/OctoberData/SP500Long.csv')[['Date', 'Price']]
# sp500.Date = sp500.Date.apply(parse_icom_date)
# sp500.Price = sp500.Price.apply(parse_float)
# sp500['Series'] = 'SP500'
# combined_data = combined_data.append(sp500, ignore_index=True, sort=False)
# print(combined_data['Date'])

combined_data = get_fred_data_as_df(combined_data, 'WTICRUDE', 'WTI.csv')
combined_data = get_fred_data_as_df(combined_data, 'GOLD', 'GOLD.csv')
combined_data = get_fred_data_as_df(combined_data, 'T10Y3M', 'T10Y3M.csv')
combined_data = get_fred_data_as_df(combined_data, 'T10Y2Y', 'T10Y2Y.csv')
combined_data = get_fred_data_as_df(combined_data, 'UNEMPLOY', 'UNEMPLOY.csv')
combined_data = get_fred_data_as_df(combined_data, 'FEDFUNDS', 'FEDFUNDS.csv')
combined_data = get_fred_data_as_df(combined_data, 'DELINQUENCY', 'DELINQUENCY.csv')
combined_data = get_fred_data_as_df(combined_data, 'GDP', 'USGDPLong.csv')
combined_data = get_fred_data_as_df(combined_data, 'SP500', 'SP500Long.csv')


combined_data = combined_data[combined_data['Price'] != '.']
combined_data.Date = combined_data.Date.apply(parseDate)

# print(combined_data[['Date', 'Series']].groupby('Series').max())
# print(combined_data[['Date', 'Series']].groupby('Series').min())


def latest_sample(data, date):
    data = data[data['Date'] <= date]
    return data.sort_values('Date', ascending=False).drop_duplicates(subset='Series')


start_date = parseDate('2019-06-06')
end_date = parseDate('2019-11-28')
next_date = start_date
sample = pd.DataFrame()
while next_date <= end_date:
    print(next_date)
    sampled_data = latest_sample(combined_data, next_date)
    print(sampled_data)
    sampled_data['Date'] = next_date
    sample = sample.append(sampled_data, ignore_index=True)
    next_date = next_date + relativedelta(days = 7)


sample.to_csv('/Users/ashwin/PycharmProjects/ResearchPaper/RawData/NovemberData/SampledData_November.csv', index=False)