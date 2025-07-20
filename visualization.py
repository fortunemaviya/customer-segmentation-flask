import matplotlib.pyplot as plt
import seaborn as sns

def plot_elbow(wcss):
    plt.figure(figsize=(8, 5))
    plt.plot(range(1, 11), wcss, 'bo-')
    plt.title('Elbow Method for Optimal Clusters')
    plt.xlabel('Number of clusters')
    plt.ylabel('Inertia')
    plt.grid(True)
    plt.show()

def plot_clusters(df, kmeans):
    plt.figure(figsize=(10, 6))
    plt.scatter(df['Annual Income (k$)'], df['Spending Score (1-100)'],
                c=kmeans.labels_, cmap='rainbow')
    plt.title('Customer Clusters')
    plt.xlabel('Annual Income (k$)')
    plt.ylabel('Spending Score (1–100)')
    plt.colorbar(label='Cluster')
    plt.show()

def plot_income_vs_spending(df):
    plt.figure(figsize=(10, 6))
    sns.scatterplot(
        x='Annual Income (k$)', y='Spending Score (1-100)',
        hue='Clusters', data=df, palette='viridis', s=100
    )
    plt.title('Income vs. Spending Score by Cluster')
    plt.show()

def plot_age_distribution(df):
    plt.figure(figsize=(10, 6))
    sns.boxplot(x='Clusters', y='Age', data=df)
    plt.title('Age Distribution by Cluster')
    plt.show()

def plot_cluster_heatmaps(df):
    for cluster in sorted(df['Clusters'].unique()):
        cluster_data = df[df['Clusters'] == cluster]
        corr = cluster_data[['Age', 'Annual Income (k$)', 'Spending Score (1-100)']].corr()
        plt.figure(figsize=(5, 4))
        sns.heatmap(corr, annot=True, fmt=".2f", cmap='coolwarm')
        plt.title(f'Cluster {cluster} Correlation Heatmap')
        plt.show()
