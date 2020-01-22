
import numpy as np
import pandas as pd

from DateParseres import parse_excel_date
from clustering.ClusteringModel import get_empty_named_cluster_assignments, assign_out_of_sample_clusters, \
    reassign_cluster_center

cluster_df = pd.read_csv('ClustersValidation.csv')
cluster_df.set_index('Date', inplace=True)
centers = cluster_df.groupby('Cluster').mean()

combined_data = pd.read_csv('SampledData.csv')
combined_data.Date = combined_data.Date.apply(parse_excel_date)
combined_data = combined_data.pivot_table(values='Price', index='Date', columns='Series')
combined_data.sort_index(inplace=True)
two_year_average = combined_data.rolling(window=100).agg(np.mean)
two_month_average = combined_data.rolling(window=16).agg(np.mean)
momentum = ((two_month_average - two_year_average)/two_year_average).dropna()

new_data = momentum[momentum.index >= parseDate("07/01/2019")]
new_data = new_data.sort_index()
clusters = get_empty_named_cluster_assignments(len(centers.index))

print(centers)
for date in new_data.index:
    data_point = new_data.loc[date]
    print(date)
    cluster = assign_out_of_sample_clusters(data_point, centers)
    cluster_df = cluster_df.append(data_point)
    clusters[cluster] = np.append(clusters[cluster], date)
    reassign_cluster_center(cluster_df, clusters, centers)


cluster_df = pd.DataFrame()
for cluster in clusters:
    for date in clusters[cluster]:
        series = pd.Series()
        series['Cluster'] = str(cluster)
        series['Date'] = date
        cluster_df = cluster_df.append(series, ignore_index=True)
#
cluster_df.set_index('Date', inplace=True)
cluster_data = cluster_df.join(momentum, how='inner')
# cluster_df = cluster_df.join(momentum, how='inner',rsuffix='momentum')
cluster_data.to_csv('ClustersValidation_November.csv')
centers.to_csv('CentersValidation_November.csv')
