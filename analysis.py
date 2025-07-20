def get_age_stats(df):
    return df.groupby('Clusters')['Age'].agg([
        ('Min Age', 'min'),
        ('Max Age', 'max'),
        ('Age Range', lambda x: x.max() - x.min()),
        ('Modal Age', lambda x: x.mode()[0]),
        ('Mean Age', 'mean'),
        ('Median Age', 'median')
    ]).reset_index()

def get_cluster_stats(df):
    stats = df.groupby('Clusters').agg({
        'Annual Income (k$)': ['min', 'max', 'mean', 'median', 'std'],
        'Spending Score (1-100)': ['min', 'max', 'mean', 'median', 'std']
    }).reset_index()

    stats.columns = [
        'Cluster',
        'Min Income', 'Max Income', 'Avg Income', 'Median Income', 'Income Std',
        'Min Spending', 'Max Spending', 'Avg Spending', 'Median Spending', 'Spending Std'
    ]
    return stats
