# 🧠 Customer Segmentation Web App

[![Python](https://img.shields.io/badge/Python-3.10-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0-blue.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

This Flask application performs customer segmentation using K-Means clustering. Users can upload customer data in CSV format, specify the number of clusters, and visualize the results.

<img width="1895" height="952" alt="image" src="https://github.com/user-attachments/assets/168aebaf-4fb3-48dd-84d1-0a66c960dc82" />
<img width="1891" height="873" alt="image" src="https://github.com/user-attachments/assets/5312402a-f0d3-468c-b8f0-cfff14f5d63a" />

the above results are easily interpretable for business cases therefore making it vital for businesses in their bid to understand the market and how to tailr products in that regards.


## Features

- CSV file upload with validation
- Interactive cluster visualization
- Downloadable segmentation results
- Model persistence with joblib
- Responsive Bootstrap UI
- Ready for deployment

## Project Structure

```
customer-segmentation-flask/
├── app.py                # Main application
├── clustering.py         # ML model logic
├── requirements.txt      # Dependencies
├── Procfile              # Deployment config
├── runtime.txt           # Python version
├── uploads/              # User uploads
├── static/               # Assets & plots
└── templates/            # HTML templates
```

## Installation

```bash
git clone https://github.com/<your-username>/customer-segmentation-flask.git
cd customer-segmentation-flask
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Usage

```bash
python app.py
```

Visit `http://localhost:5000` in your browser.

1. Upload a CSV file with customer data
2. Specify number of clusters (K)
3. View and download results

## Data Format

Your CSV should contain at least these columns:

| CustomerID | Annual Income (k$) | Spending Score (1-100) |
|------------|--------------------|------------------------|
| 1          | 15                 | 39                     |
| 2          | 15                 | 81                     |

## Deployment

### Heroku

1. Create new Heroku app
2. Connect to your GitHub repository
3. Deploy branch

### Render

1. Create new Web Service
2. Connect repository
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `gunicorn app:app`

## License

This project is licensed under the MIT License - see [LICENSE](LICENSE) for details.
