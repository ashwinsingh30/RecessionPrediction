import datetime
import pandas as pd
from matplotlib import pyplot as plt
import numpy as np

def savitzky_golay(y, window_size, order, deriv=0, rate=1):
    from math import factorial

    try:
        window_size = np.abs(np.int(window_size))
        order = np.abs(np.int(order))
    except ValueError:
        raise ValueError("window_size and order have to be of type int")
    if window_size % 2 != 1 or window_size < 1:
        raise TypeError("window_size size must be a positive odd number")
    if window_size < order + 2:
        raise TypeError("window_size is too small for the polynomials order")
    order_range = range(order + 1)
    half_window = (window_size - 1) // 2
    b = np.mat([[k ** i for i in order_range] for k in range(-half_window, half_window + 1)])
    m = np.linalg.pinv(b).A[deriv] * rate ** deriv * factorial(deriv)
    firstvals = y[0] - np.abs(y[1:half_window + 1][::-1] - y[0])
    lastvals = y[-1] + np.abs(y[-half_window - 1:-1][::-1] - y[-1])
    y = np.concatenate((firstvals, y, lastvals))
    return np.convolve(m[::-1], y, mode='valid')


def parse_date(date):
    date = date.split("-")
    m = date[1]
    # if(int(m)<10):
    #     m="0"+m
    d = date[2]
    y = date[0]
    return datetime.datetime.strptime(d+m+y, "%d%m%Y").date()


# series = 'Combined Model'
# period = 'TruePositivePredictionProb'

# baseline_data_3M = pd.read_csv('BaselinePrediction3Months.csv')
# baseline_data_3M.Date = baseline_data_3M.Date.apply(parse_date)
# baseline_data_3M = baseline_data_3M.set_index('Date')
# baseline_data_3M = baseline_data_3M[(baseline_data_3M.index>=parse_date('2005-01-01')) &
#                               (baseline_data_3M.index<=parse_date('2019-03-01'))][period]
# baseline_data_3M.name = '3 Months Transition'
#
# baseline_data_6M = pd.read_csv('BaselinePrediction6Months.csv')
# baseline_data_6M.Date = baseline_data_6M.Date.apply(parse_date)
# baseline_data_6M = baseline_data_6M.set_index('Date')
# baseline_data_6M = baseline_data_6M[(baseline_data_6M.index>=parse_date('2005-01-01')) &
#                               (baseline_data_6M.index<=parse_date('2019-03-01'))][period]
# baseline_data_6M.name = '6 Months Transition'
#
# baseline_data_9M = pd.read_csv('BaselinePrediction9Months.csv')
# baseline_data_9M.Date = baseline_data_9M.Date.apply(parse_date)
# baseline_data_9M = baseline_data_9M.set_index('Date')
# baseline_data_9M = baseline_data_9M[(baseline_data_9M.index>=parse_date('2005-01-01')) &
#                               (baseline_data_9M.index<=parse_date('2019-03-01'))][period]
# baseline_data_9M.name = '9 Months Transition'
#
# baseline_data_12M = pd.read_csv('BaselinePrediction12Months.csv')
# baseline_data_12M.Date = baseline_data_12M.Date.apply(parse_date)
# baseline_data_12M = baseline_data_12M.set_index('Date')
# baseline_data_12M = baseline_data_12M[(baseline_data_12M.index>=parse_date('2005-01-01')) &
#                               (baseline_data_12M.index<=parse_date('2019-03-01'))][period]
# baseline_data_12M.name = '12 Months Transition'
#
# combined_data = pd.concat([baseline_data_3M, baseline_data_6M, baseline_data_9M, baseline_data_12M], axis=1)
#
# for column in combined_data.columns:
#     combined_data[column] = pd.Series(savitzky_golay(combined_data[column],9,5), index=combined_data[column].index)
#
#
# # plt.figure(figsize=(12,5))
# # title = series + " " + "True Positive Predictions"
# # plt.title(title)
# # plt.xlabel('Date')
# # plt.ylabel('Transition Probability')
#
# ax = combined_data.plot()
# title = series + " " + "True Positive Predictions"
# plt.title(title)
# plt.xlabel('Date')
# plt.ylabel('Transition Probability')
# ax.set_ylim(0,0.8)
#
# # ax1 = baseline_data_3M.plot(color='red', grid=True, label='3 Months Transition')
# # ax1.set(ylim=(0,0.8))
# # ax2 = baseline_data_6M.plot(color='blue', grid=True, label='6 Months Transition')
# # ax2.set(ylim=(0,0.8))
# # ax3 = baseline_data_9M.plot(color='green', grid=True, label='9 Months Transition')
# # ax3.set(ylim=(0,0.8))
# # ax4 = baseline_data_12M.plot(color='green', grid=True, label='12 Months Transition')
# # ax4.set(ylim=(0,0.8))
# # h1, l1 = ax1.get_legend_handles_labels()
# # h2, l2 = ax2.get_legend_handles_labels()
# # h3, l3 = ax3.get_legend_handles_labels()
# # h4, l4 = ax4.get_legend_handles_labels()
# #
# #
# # plt.legend(h1, l1, loc=1)
# plt.show()


series = 'Combined Model'
period = 'TruePositivePredictionProb'
#
#
baseline_data = pd.read_csv('BaselinePrediction3Months.csv')
baseline_data.Date = baseline_data.Date.apply(parse_date)
baseline_data = baseline_data.set_index('Date')

transition_probabilities = pd.read_csv('CombinedPrediction3Months_2007.csv')
transition_probabilities.Date = transition_probabilities.Date.apply(parse_date)
transition_probabilities = transition_probabilities.set_index('Date')


baseline_data = baseline_data[(baseline_data.index>=parse_date('2005-01-01')) &
                              (baseline_data.index<=parse_date('2008-01-01'))][period]
transition_probabilities = transition_probabilities[(transition_probabilities.index>=parse_date('2005-01-01')) &
                              (transition_probabilities.index<=parse_date('2008-01-01'))][period]

print(baseline_data)
print(transition_probabilities)


plt.figure(figsize=(12,5))
title = series + " " + "3 Month Transition Probabilities"
plt.title(title)
plt.xlabel('Date')
plt.ylabel('Transition Probability')

ax1 = baseline_data.plot(color='red', grid=True, label='Actual True Positive Prediction', linestyle='dashed')
ax1.set(ylim=(0,0.8))
ax2 = transition_probabilities.plot(color='blue', grid=True, secondary_y=True, label='Transition Probability to Recession State')
ax2.set(ylim=(0,0.8))
h1, l1 = ax1.get_legend_handles_labels()
h2, l2 = ax2.get_legend_handles_labels()


plt.legend(h1+h2, l1+l2, loc=2)
plt.show()


# plot_data = baseline_data['12Month']
# plot_data = pd.Series(savitzky_golay(baseline_data['12Month'],9,5), index= baseline_data['3Month'].index)
# plot_data.plot()
# data.set_index('Date', inplace=True, drop=True)
# data = data[data.index >= parse_date('2008-06-01')]
# data.sort_index(inplace=True)
# data['GrowthRate'] = data['Price'].pct_change(periods=4)*100
# print(data['GrowthRate'].mean())
# data['GrowthRate'].plot()
# print(data)
# plt.axhline(y=0, color='red', linestyle='dashed')
# plt.show()

