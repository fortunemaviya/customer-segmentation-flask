import os
import shutil
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from flask import Flask, render_template, request, send_file
import pandas as pd
import seaborn as sns
from clustering import preprocess_data, train_kmeans, save_model

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['STATIC_FOLDER'] = 'static'

# Create folders if not exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['STATIC_FOLDER'], exist_ok=True)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/segment', methods=['POST'])
def segment():
    try:
        # Clear previous files
        for folder in [app.config['UPLOAD_FOLDER'], app.config['STATIC_FOLDER']]:
            for filename in os.listdir(folder):
                file_path = os.path.join(folder, filename)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                except Exception as e:
                    print(f'Error deleting {file_path}: {e}')
        
        # Process form data
        file = request.files['file']
        k = int(request.form['k'])
        save_option = 'save_model' in request.form
        
        # Save uploaded file
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        
        # Load and process data
        df = pd.read_csv(file_path)
        X_scaled, income_col, score_col = preprocess_data(df)
        
        # Train model
        model = train_kmeans(X_scaled, k)
        labels = model.predict(X_scaled)
        df['Cluster'] = labels
        
        # Save model if requested
        if save_option:
            save_model(model)
        
        # Generate plot
        plt.figure(figsize=(10, 8))
        plt.scatter(df[income_col], df[score_col], c=labels, cmap='viridis', s=100, alpha=0.8)
        plt.title(f'Customer Segments (K={k})', fontsize=14)
        plt.xlabel(income_col, fontsize=12)
        plt.ylabel(score_col, fontsize=12)
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.colorbar(label='Cluster ID')
        
        plot_path = os.path.join(app.config['STATIC_FOLDER'], 'cluster_plot.png')
        plt.savefig(plot_path, bbox_inches='tight')
        plt.close()
        
        # Save results
        result_path = os.path.join(app.config['UPLOAD_FOLDER'], 'segmented_data.csv')
        df.to_csv(result_path, index=False)
        
        # Calculate statistics
        total_customers = len(df)
        avg_income = df[income_col].mean().round(1)
        avg_score = df[score_col].mean().round(1)
        
        # Generate cluster colors
        viridis = matplotlib.colormaps['viridis']
        cluster_colors = [matplotlib.colors.to_hex(viridis(i/k)) for i in range(k)]
        
        # Calculate cluster sizes
        cluster_counts = df['Cluster'].value_counts().sort_index()
        cluster_sizes = cluster_counts.tolist()
        
        # Prepare cluster details
        cluster_details = []
        for cluster_id in range(k):
            cluster_data = df[df['Cluster'] == cluster_id]
            size = len(cluster_data)
            
            # Income stats
            income_min = cluster_data[income_col].min()
            income_max = cluster_data[income_col].max()
            income_avg = cluster_data[income_col].mean().round(1)
            
            # Score stats
            score_min = cluster_data[score_col].min()
            score_max = cluster_data[score_col].max()
            score_avg = cluster_data[score_col].mean().round(1)
            
            # Determine profile based on metrics
            if income_avg > avg_income and score_avg > avg_score:
                profile = "High-value customers (Big spenders with good income)"
            elif income_avg > avg_income and score_avg < avg_score:
                profile = "Conservative customers (High income but low spending)"
            elif income_avg < avg_income and score_avg > avg_score:
                profile = "Budget enthusiasts (Low income but high spending)"
            elif income_avg < avg_income and score_avg < avg_score:
                profile = "Low engagement (Low income and low spending)"
            else:
                profile = "Average customers"
            
            cluster_details.append({
                'size': size,
                'income_min': income_min,
                'income_max': income_max,
                'income_avg': income_avg,
                'income_pct': (income_avg / df[income_col].max()) * 100,
                'score_min': score_min,
                'score_max': score_max,
                'score_avg': score_avg,
                'score_pct': (score_avg / 100) * 100,
                'profile': profile
            })
        
        # Generate summary statistics table
        cluster_stats = df.groupby('Cluster').agg({
            income_col: ['min', 'max', 'mean', 'median', 'count'],
            score_col: ['min', 'max', 'mean', 'median']
        }).round(2)
        
        # Flatten multi-level columns
        cluster_stats.columns = ['_'.join(col).strip() for col in cluster_stats.columns.values]
        cluster_stats.reset_index(inplace=True)
        cluster_stats.rename(columns={f'{income_col}_count': 'Count'}, inplace=True)
        
        # Render template with all data
        return render_template(
            'result.html',
            k=k,
            plot_url=f"static/cluster_plot.png?t={os.path.getmtime(plot_path)}",
            tables=[df.sample(min(5, len(df))).to_html(classes='table table-striped', index=False)],
            stats=cluster_stats.to_html(classes='table table-hover', index=False),
            total_customers=total_customers,
            avg_income=avg_income,
            avg_score=avg_score,
            cluster_sizes=cluster_sizes,
            cluster_colors=cluster_colors,
            cluster_details=cluster_details,
            sample_size=min(5, len(df))
        )
        
    except Exception as e:
        error_msg = f"Error processing file: {str(e)}"
        print(error_msg)
        return render_template('index.html', error=error_msg)

@app.route('/download')
def download():
    return send_file(
        os.path.join(app.config['UPLOAD_FOLDER'], 'segmented_data.csv'),
        as_attachment=True,
        download_name='customer_segments.csv'
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)