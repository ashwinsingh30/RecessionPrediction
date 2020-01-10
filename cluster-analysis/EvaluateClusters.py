import datetime
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

clusters = pd.read_csv('ClustersValidation.csv')
# forward_looking = pd.read_csv('ForwardLookingReturns.csv')

def parseDate(date):
    date = date.split("/")
    m = date[1]
    # if(int(m)<10):
    #     m="0"+m
    d = date[0]
    if int(date[2]) > 80:
        y = "19"+date[2]
    else:
        y = "20" + date[2]
    return str(datetime.datetime.strptime(m + d + y, "%m%d%Y").date())

def parse_date(date):
    return datetime.datetime.strptime(date, '%Y-%m-%d').date()

clusters.Date = clusters.Date.apply(parseDate)
clusters.set_index('Date', inplace=True, drop=True)
# forward_looking.set_index('Date', inplace=True, drop=True)

raw_data = pd.read_csv('SamplePivoted.csv')
# raw_data.Date = raw_data.Date.apply(parse_date)
raw_data.set_index('Date', inplace=True)

nifty_sample = pd.read_csv('NiftySample.csv')
nifty_sample.set_index('Date', inplace=True)
# raw_data = raw_data.join(nifty_sample, how='inner')

raw_data.sort_index(ascending=False, inplace=True)
# diff = -1 * raw_data.pct_change(periods=50)
diff = (-1 * (raw_data.diff(periods=50) / raw_data.abs()))
# cluster_names = clusters.Cluster.unique()
# cluster_time = pd.DataFrame()
#
# previous_cluster = clusters.iloc[0]['Cluster']
# start_date = clusters.index[0]
# ctr = 1
# for index in clusters.index:
#     current_cluster = clusters.loc[index]['Cluster']
#     if current_cluster != previous_cluster:
#         if ctr >= 4:
#             cluster_transition = pd.Series()
#             cluster_transition['Cluster'] = previous_cluster
#             cluster_transition['StartTime'] = start_date
#             cluster_transition['EndTime'] = index
#             cluster_time = cluster_time.append(cluster_transition, ignore_index=True)
#         ctr=1
#         previous_cluster = current_cluster
#         start_date = index
#     else:
#         ctr+=1
#
# cluster_time.to_csv('/Users/ashwin/PycharmProjects/ClustersByTimePeriod.csv')

pre_recession = clusters
# pre_recession = clusters[clusters['Condition'].isin(['Pre Recession'])]
# pre_recession = pre_recession.drop('Condition', axis=1)
# print(np.intersect1d(pre_recession.index, forward_looking.index))
# pre_recession = pre_recession.join(diff, how='inner', rsuffix = '_returns')
# print(pre_recession)
# pre_recession = pre_recession[(pre_recession.index > parseDate('01/01/00')) &
#                               (pre_recession.index < parseDate('01/03/02'))]
# pre_recession['DELINQUENCY'].plot()
# axes = plt.gca()
# axes.set_ylim([-10, 10])
# plt.axhline(y=0, color='red')
# plt.show()
# pre_recession = pre_recession.dropna(axis=0)
# pre_recession.to_csv('JoinedData.csv')
# pre_recession_centers = pre_recession.groupby('Cluster').std()
# print(pre_recession.drop('Condition', axis=1).groupby('Cluster').mean())
# pre_recession_centers.to_csv('ClusterSTD.csv')
print(pre_recession.std())

# centers = pd.read_csv('CentersValidation.csv', index_col=[0])
# print(centers)
# cluster_distances = {}
# for index1 in centers.index:
#     distances = {}
#     for index2 in centers.index:
#         print(centers.loc[index1])
#         distances[index2] = np.linalg.norm(centers.loc[index1] - centers.loc[index2])
#     cluster_distances[index1] = distances
#
# print(pd.DataFrame(cluster_distances).to_csv('ClusterDistances.csv'))
