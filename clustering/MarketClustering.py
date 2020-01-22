import math

import datetime
import numpy as np
import pandas as pd
import random
from matplotlib import pyplot as plt
import nltk
from dateutil.relativedelta import relativedelta




# combined_data = pd.read_csv('SampledData.csv')
# combined_data.Date = combined_data.Date.apply(parseDate2)
# combined_data = combined_data.pivot_table(values='Price', index='Date', columns='Series')
# combined_data.sort_index(inplace=True)
# print(combined_data)
# # combined_data = -1 * combined_data.pct_change(periods=50)
# # combined_data.to_csv('ForwardLookingReturns.csv')
# two_year_average = combined_data.rolling(window=100).agg(np.mean)
# two_month_average = combined_data.rolling(window=16).agg(np.mean)
# momentum = ((two_month_average - two_year_average)/two_year_average).dropna()
# momentum.to_csv('DataNormalised_November.csv')
# # momentum.plot()
# # axes = plt.gca()
# # axes.set_ylim([-1, 1])
# # plt.show()
#
# clusters, centers = cluster_data(momentum,15)
# cluster_df = pd.DataFrame()
# for cluster in clusters:
#     for date in clusters[cluster]:
#         series = pd.Series()
#         series['Cluster'] = 'cluster_' + str(cluster)
#         series['Date'] = date
#         cluster_df = cluster_df.append(series, ignore_index=True)

# cluster_df = pd.read_csv('ClustersValidation.csv')
# cluster_df.set_index('Date', inplace=True)
# # in_sample = momentum[momentum.index < parseDate("01/01/2015")]
# # clustered_data = cluster_data[cluster_data.index <  parseDate("01/01/2015")]
# # centers = clustered_data.groupby('Cluster').mean()
# centers = cluster_df.groupby('Cluster').mean()
#
# out_sample = momentum[momentum.index >= parseDate("07/01/2019")]
# out_sample = out_sample.sort_index()
# clusters = get_empty_named_cluster_assignments(len(centers.index))
# # for date in in_sample.index:
# #     cluster = cluster_df.loc[date]['Cluster']
# #     clusters[cluster] = np.append(clusters[cluster], date)
#
# print(centers)
# for date in out_sample.index:
#     data_point = out_sample.loc[date]
#     print(date)
#     cluster = assign_out_of_sample_clusters(data_point, centers)
#     # in_sample = in_sample.append(data_point)
#     clusters[cluster] = np.append(clusters[cluster], date)
# #     reassign_cluster_center(in_sample, clusters, centers)
# #
# #
# cluster_df = pd.DataFrame()
# for cluster in clusters:
#     for date in clusters[cluster]:
#         series = pd.Series()
#         series['Cluster'] = str(cluster)
#         series['Date'] = date
#         cluster_df = cluster_df.append(series, ignore_index=True)
# #
# cluster_df.set_index('Date', inplace=True)
# cluster_data = cluster_df.join(momentum, how='inner')
# # cluster_df = cluster_df.join(momentum, how='inner',rsuffix='momentum')
# cluster_data.to_csv('ClustersValidation_November.csv')
# centers.to_csv('CentersValidation_November.csv')


#
# centers = pd.read_csv('Centers2.csv', index_col=[0])
# print(centers)
# distance_df = pd.DataFrame(index = centers.index, columns=centers.index)
#
# for index1 in centers.index:
#     for index2 in centers.index:
#         distance_df[index1][index2] = np.linalg.norm(centers.loc[index1] - centers.loc[index2])
#
# distance_df.to_csv('Distance.csv')


# def get_bigram_most_probable(list):
#     bigram = nltk.bigrams(list)
#     condition_pairs = ((w0, w1) for w0, w1 in bigram)
#     cfd = nltk.ConditionalFreqDist(condition_pairs)
#     return cfd
#
#
from DateParseres import parse_excel_date

clusters = pd.read_csv('/Users/ashwin/PycharmProjects/RecessionPrediction/processed-data/ClustersValidation.csv')
clusters.Date = clusters.Date.apply(parse_excel_date)
clusters = clusters.set_index('Date').sort_index()
print(clusters)
cluster_names = clusters.Cluster.unique()
cluster_time = {}
for cluster in cluster_names:
    cluster_time[cluster] = np.array([])

previous_cluster = clusters.iloc[0]['Cluster']
ctr = 1
for index in clusters.index:
    current_cluster = clusters.loc[index]['Cluster']
    if current_cluster != previous_cluster:
        if ctr >= 4:
            cluster_time[previous_cluster] = np.append(cluster_time[previous_cluster], ctr)
        ctr=1
        previous_cluster = current_cluster
    else:
        ctr+=1

print(cluster_time)
#
# for cluster in cluster_time:
#     print(cluster, np.mean(cluster_time[cluster]), np.std(cluster_time[cluster]))

# combined_data = pd.read_csv('SampleCombined.csv')
# # print(combined_data[['Asset', 'Price']].groupby(['Asset']).std())
# # print(clusters.groupby(['Cluster']).std().mean())
#
# combined_data = combined_data.pivot_table(values='Price', index='Date', columns='Asset')
# combined_data = combined_data.sort_index().pct_change()
# combined_data['Cluster'] = clusters['Cluster']
# print(clusters.groupby('Cluster').count())
# (combined_data.groupby('Cluster').std() * np.sqrt(50)).to_csv('ClusterVolatilities.csv')
#
# clusters = clusters.sort_index()
# print(clusters)
# # clusters.to_csv('Sorted.csv')
# # clusters[['crude','gold','nifty','sp500','teny_to_3m','teny_to_twoy','twoy','unemployment']] = \
# #     clusters[['crude','gold','nifty','sp500','teny_to_3m','teny_to_twoy','twoy','unemployment']].pct_change(periods=-50)
# data = clusters[['crude','gold','nifty','sp500','teny_to_3m','teny_to_twoy','twoy','unemployment']]
#
# data = ((data.shift(-50) - data)/data)
# clusters[['crude','gold','nifty','sp500','teny_to_3m','teny_to_twoy','twoy','unemployment']] = data
# cluster_names = clusters['Cluster'].unique()
# probabilities = pd.DataFrame(index=cluster_names, columns=cluster_names)
# clusters = clusters.sort_index()
# cluster_names = clusters['Cluster'].unique()
# bigrams = get_bigram_most_probable(clusters['Cluster'])
# for cluster_name1 in cluster_names:
#     for cluster_name2 in cluster_names:
#         print(bigrams[cluster_name1])
#         print(cluster_name1, len(clusters[clusters['Cluster']==cluster_name1].index))
#         probabilities.loc[cluster_name1][cluster_name2] = \
#             bigrams[cluster_name1][cluster_name2] / len(clusters[clusters['Cluster']==cluster_name1].index)
# probabilities = probabilities.reindex(sorted(probabilities.columns), axis=1)
# probabilities = probabilities.sort_index()
# print(probabilities.to_csv('TransitionProbs.csv'))
# # print(pd.DataFrame(np.linalg.matrix_power(probabilities, 100), index = probabilities.index, columns=probabilities.columns).to_csv('TransitionProbs.csv'))
# clusters = clusters.groupby(['Cluster']).mean()
# print(clusters[['nifty', 'sp500']])
#
#
#


