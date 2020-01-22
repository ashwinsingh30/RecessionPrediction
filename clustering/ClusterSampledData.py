import pandas as pd
import numpy as np

from DateParseres import parse_python_date_format
from clustering.ClusteringModel import create_clusters, get_empty_named_cluster_assignments, assign_out_of_sample_clusters, \
    reassign_cluster_center

combined_data = pd.read_csv('/Users/ashwin/PycharmProjects/RecessionPrediction/processed-data/SampledData.csv')
combined_data.Date = combined_data.Date.apply(parse_python_date_format)
combined_data = combined_data.pivot_table(values='Price', index='Date', columns='Series')
combined_data.sort_index(inplace=True)
# combined_data = combined_data[combined_data.index <= parse_python_date_format('2019-06-30')]
print(combined_data)
# combined_data = -1 * combined_data.pct_change(periods=50)
# combined_data.to_csv('ForwardLookingReturns.csv')
two_year_average = combined_data.rolling(window=100).agg(np.mean)
two_month_average = combined_data.rolling(window=16).agg(np.mean)
momentum = ((two_month_average - two_year_average)/two_year_average).dropna()
momentum.to_csv('/Users/ashwin/PycharmProjects/RecessionPrediction/processed-data/DataNormalised_January.csv')

clusters, centers = create_clusters(momentum, 15)
cluster_df = pd.DataFrame()
for cluster in clusters:
    for date in clusters[cluster]:
        series = pd.Series()
        series['Cluster'] = 'cluster_' + str(cluster)
        series['Date'] = date
        cluster_df = cluster_df.append(series, ignore_index=True)

cluster_df.set_index('Date', inplace=True)
cluster_df = cluster_df.join(momentum, how='inner')

cluster_data = cluster_df.join(combined_data, how='inner',rsuffix='_raw')
cluster_data.to_csv('/Users/ashwin/PycharmProjects/RecessionPrediction/processed-data/ClusterTotal_January.csv')
centers.to_csv('/Users/ashwin/PycharmProjects/RecessionPrediction/processed-data/CentersTotal_January.csv')
data_separation_date = "2016-01-01"

in_sample = momentum[momentum.index < parse_python_date_format(data_separation_date)]
clustered_data = cluster_df[cluster_df.index < parse_python_date_format(data_separation_date)]
centers_in_sample = clustered_data.groupby('Cluster').mean()

out_sample = momentum[momentum.index >= parse_python_date_format(data_separation_date)]
out_sample = out_sample.sort_index()
clusters = get_empty_named_cluster_assignments(len(centers.index))

for date in in_sample.index:
    cluster = cluster_df.loc[date]['Cluster']
    clusters[cluster] = np.append(clusters[cluster], date)


for date in out_sample.index:
    data_point = out_sample.loc[date]
    cluster = assign_out_of_sample_clusters(data_point, centers_in_sample)
    in_sample = in_sample.append(data_point)
    clusters[cluster] = np.append(clusters[cluster], date)
    reassign_cluster_center(in_sample, clusters, centers_in_sample)

cluster_df = pd.DataFrame()
for cluster in clusters:
    for date in clusters[cluster]:
        series = pd.Series()
        series['Cluster'] = str(cluster)
        series['Date'] = date
        cluster_df = cluster_df.append(series, ignore_index=True)

cluster_df.set_index('Date', inplace=True)
cluster_df = cluster_df.join(momentum, how='inner')
cluster_df.to_csv('/Users/ashwin/PycharmProjects/RecessionPrediction/processed-data/Clusters_January.csv')
centers_in_sample.to_csv('/Users/ashwin/PycharmProjects/RecessionPrediction/processed-data/Centers_January.csv')