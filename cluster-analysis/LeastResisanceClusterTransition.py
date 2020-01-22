import datetime
import numpy as np
import pandas as pd
from dateutil.relativedelta import relativedelta


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
    return datetime.datetime.strptime(m + d + y, "%m%d%Y").date()

def parse_date(date):
    return datetime.datetime.strptime(date, '%Y-%m-%d').date()

# centers = pd.read_csv('/Users/ashwin/PycharmProjects/ResearchPaper/RecessionaryCenters.csv', index_col=[0])
clusters = pd.read_csv('/Users/ashwin/PycharmProjects/RecessionPrediction/processed-data/Clusters_January.csv')
clusters.Date = clusters.Date.apply(parseDate)
clusters.set_index('Date', inplace=True)
cluster_series = clusters['Cluster']
raw_data = pd.read_csv('/Users/ashwin/PycharmProjects/RecessionPrediction/processed-data/DataNormalised_January.csv')
raw_data.Date = raw_data.Date.apply(parse_date)
raw_data.set_index('Date', inplace=True)


def get_correlation_matrix(cluster, date):
    val_series = clusters[clusters.index <= date]
    val_series = val_series[val_series['Cluster'] == cluster]
    val_series = val_series.drop('Cluster', axis=1)
    return val_series.corr()

def get_current_momentum(date):
    return raw_data.loc[date]

def get_n_month_change_distribution(n, date):
    data = raw_data.loc[raw_data.index <= (date + relativedelta(years=1))]
    data.sort_index(ascending=False, inplace=True)
    diff = (-1 * (data.diff(periods=5*n)/data.abs()))
    diff = diff.dropna(axis=0)
    return diff


# clusters = clusters[clusters['Cluster'] == 'cluster_6']
# val_series = clusters[clusters['Date'] <= parseDate('01/01/07')]
# val_series = val_series.drop('Date', axis=1)
# val_series = clusters.drop('Date', axis=1)
# val_series = val_series[val_series['Cluster'] == 'cluster_6']
# val_series = val_series.drop('Cluster', axis=1)
# correlation_matrix = val_series.corr()
# print(correlation_matrix)
# raw_data = raw_data.sort_index(ascending=False).head(100).mean()
# print(raw_data)

cluster_transitions = pd.DataFrame()
transition_momentum = pd.DataFrame()
transition_probabilities = pd.DataFrame()

def get_transition_threshod(date, current_datapoint , current_center, transition_center):
    correlation_matrix = get_correlation_matrix(current_center.name, date)
    change_3m = get_n_month_change_distribution(3, date)
    change_6m = get_n_month_change_distribution(6, date)
    change_9m = get_n_month_change_distribution(9, date)
    change_12m = get_n_month_change_distribution(12, date)
    global transition_probabilities
    transition_value_series = pd.Series()
    transition_value_series['CurrentCluster'] = current_center.name
    transition_value_series['TransitionCluster'] = transition_center.name
    transition_value_series['Date'] = date
    transition_momentum_series = pd.Series(transition_value_series)
    transition_probability_series = pd.Series(transition_value_series)
    S1 = ((current_center ** 2) - (transition_center ** 2)).sum()
    S2 = 2 * (current_datapoint * (current_center - transition_center)).sum()
    for series in current_datapoint.index:
        transition_probability_series['Series'] = series
        c_k = current_datapoint.loc[series]
        corr_vector = correlation_matrix.loc[series]
        S3 = 2 * (corr_vector * (current_center - transition_center)).sum()
        transition_value = ((S1 - S2) / S3) + c_k
        transition_value_series[series] = (transition_value * (raw_data[series] + 1))
        transition_momentum_series[series] = transition_value
        delta = (transition_value - current_datapoint[series]) / np.abs(current_datapoint[series])
        if delta > 0:
            transition_probability_series['3Month'] = len(change_3m[change_3m[series] >= delta].index)/len(change_3m.index)
            transition_probability_series['6Month'] = len(change_6m[change_6m[series] >= delta].index) / len(
                change_6m.index)
            transition_probability_series['9Month'] = len(change_9m[change_9m[series] >= delta].index) / len(
                change_9m.index)
            transition_probability_series['12Month'] = len(change_12m[change_12m[series] >= delta].index) / len(
                change_12m.index)
        else:
            transition_probability_series['3Month'] = len(change_3m[change_3m[series] <= delta].index)/len(change_3m.index)
            transition_probability_series['6Month'] = len(change_6m[change_6m[series] <= delta].index) / len(
                change_6m.index)
            transition_probability_series['9Month'] = len(change_9m[change_9m[series] <= delta].index) / len(
                change_9m.index)
            transition_probability_series['12Month'] = len(change_12m[change_12m[series] <= delta].index) / len(
                change_12m.index)
        transition_probabilities = transition_probabilities.append(transition_probability_series, ignore_index=True)
    global cluster_transitions
    global transition_momentum
    cluster_transitions = cluster_transitions.append(transition_value_series, ignore_index = True)
    transition_momentum = transition_momentum.append(transition_momentum_series, ignore_index=True)


def get_n_months_future_cluster(date, n):
    clustered_data = clusters[clusters.index >= date + relativedelta(months=n)]
    if not clustered_data.empty:
        clustered_data = clustered_data.sort_index(ascending=False)
        return clustered_data.iloc[0]['Cluster']


def get_future_cluster_center(cluster_name, date, n):
    clustered_data = clusters[clusters.index <= date + relativedelta(months=2*n)]
    clustered_data = clustered_data[clustered_data['Cluster'] == cluster_name]
    if not clustered_data.empty:
        return clustered_data.mean()

test_series = cluster_series[(cluster_series.index >= parseDate('01/01/19')) &
                             (cluster_series.index <= parseDate('12/12/19'))]
for date in test_series.index:
    current_momentum = get_current_momentum(date)
    clustered_data = clusters[clusters.index <= date]
    centers = clustered_data.groupby('Cluster').mean()
    current_center_name = cluster_series.loc[date]
    current_center = centers.loc[current_center_name]
    pre_recession = clustered_data[(clustered_data['Condition'] == 'Pre Recession') &
                                   (clustered_data['Cluster'] == 'cluster_6')]
    target_center = pre_recession.mean()
    # target_cluster = get_n_months_future_cluster(date,12)
    get_transition_threshod(date, current_momentum, current_center, target_center)
    # if target_cluster is not None and target_cluster != current_center.name:
    #     target_center = get_future_cluster_center(target_cluster, date, 12)
    #     if target_center is not None:
    #         print(current_center)
    #         print(target_cluster)
    #         target_center.name = 'future-center'
    #         print(current_momentum)
    #         get_transition_threshod(date, current_momentum, current_center, target_center)

# cluster_transitions.to_csv('ClusterTransitions.csv', index=False)
# transition_momentum.to_csv('TransitionMomentum.csv', index=False)
transition_probabilities.to_csv('TransitionProbabilities2019_November.csv')


# df = transition_probabilities
# df = pd.read_csv('TransitionProbabilities2007.csv')
# prediction_baseline = pd.DataFrame()
#
# for date in df['Date'].unique():
#     max_series = pd.Series()
#     df_for_date = df[df['Date'] == date]
#     df_for_date.set_index('Series', inplace=True)
#     probability = df_for_date['12Month']
#     max_series['Predictor'] = probability.idxmax()
#     max_series['TruePositivePredictionProb'] = probability.loc[probability.idxmax()]
#     max_series['Date'] = date
#     prediction_baseline = prediction_baseline.append(max_series, ignore_index=True)
#     print(max_series)
#
# prediction_baseline.to_csv('CombinedPrediction12Months_2007.csv', index=False)
