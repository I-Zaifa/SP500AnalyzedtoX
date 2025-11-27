# Written entirely-mostly By Mssr.GPT ET Gemini
# I had to go over many iterations and such. Mercy me!

from flask import Flask, request, render_template_string
import pandas as pd
import os

app = Flask(__name__)

STYLE_BLOCK = """
<style>
    body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #ecf0f1; color: #2c3e50; margin: 0; padding: 40px 20px; display: flex; justify-content: center; min-height: 100vh; }
    .container { background: white; padding: 40px; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.08); width: 100%; max-width: 900px; text-align: center; }
    h1 { color: #2c3e50; font-size: 2rem; margin-bottom: 30px; letter-spacing: -0.5px; }
    h2 { color: #34495e; font-size: 1.4rem; margin-top: 30px; border-bottom: 2px solid #eee; padding-bottom: 10px; text-align: left; }
    form { margin: 20px 0; display: flex; flex-direction: column; align-items: center; gap: 15px; }
    input[type="text"] { padding: 15px; width: 100%; max-width: 400px; border: 2px solid #dfe6e9; border-radius: 8px; font-size: 1rem; }
    input[type="text"]:focus { border-color: #009879; outline: none; }
    input[type="submit"], .btn { padding: 12px 30px; background-color: #009879; color: white; border: none; border-radius: 8px; cursor: pointer; font-weight: 600; font-size: 1rem; text-decoration: none; display: inline-block; }
    input[type="submit"]:hover, .btn:hover { background-color: #007f67; transform: translateY(-2px); }
    .btn-secondary { background-color: #2c3e50; }
    .btn-spicy { background-color: #d35400; }
    .table-wrapper { overflow-x: auto; margin-top: 20px; border-radius: 8px; box-shadow: 0 0 20px rgba(0, 0, 0, 0.05); }
    .styled-table { border-collapse: collapse; margin: 0; font-size: 0.9rem; width: 100%; min-width: 600px; background-color: white; }
    .styled-table thead tr { background-color: #009879; color: #ffffff; text-align: left; }
    .styled-table th, .styled-table td { padding: 15px 20px; border-bottom: 1px solid #eee; }
    .styled-table tbody tr { border-bottom: 1px solid #dddddd; }
    .styled-table tbody tr:nth-of-type(even) { background-color: #f8f9fa; }
    .styled-table tbody tr:last-of-type { border-bottom: 3px solid #009879; }
</style>
"""

def search_tickers_in_files(file_paths, tickers):
    results = {}
    for file_path in file_paths:
        try:
            if os.path.isfile(file_path):
                df = pd.read_csv(file_path)
                matched_rows = pd.DataFrame()
                for ticker in tickers:
                    for column in df.columns:
                        if df[column].astype(str).str.contains(ticker, case=False, na=False).any():
                            matched_rows = pd.concat([matched_rows, df[df[column].astype(str).str.contains(ticker, case=False, na=False)]])
                if not matched_rows.empty:
                    results[file_path] = matched_rows
            else:
                pass
        except Exception as e:
            pass
    return results

def read_and_format_file(file_path):
    try:
        if os.path.isfile(file_path):
            df = pd.read_csv(file_path)
            html_table = '<div class="table-wrapper"><table class="styled-table"><thead><tr>'
            html_table += ''.join([f'<th>{col}</th>' for col in df.columns])
            html_table += '</tr></thead><tbody>'
            for index, row in df.iterrows():
                html_table += '<tr>' + ''.join([f'<td>{cell}</td>' for cell in row]) + '</tr>'
            html_table += '</tbody></table></div><br><br>'
            return html_table
        else:
            return f"<p>File not found: {file_path}</p>"
    except Exception as e:
        return f"<p>Error reading {file_path}</p>"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        raw = request.form.get('tickers') or ''
        tickers = [t.strip() for t in raw.split(',') if t.strip()]
        
        search_file_paths = [
            'average.csv',
            'analyzed_metrics_individual_r2.csv',
            'dividends_analysis.csv',
            'stocks_analyzed.csv',
        ]
        
        search_results = search_tickers_in_files(search_file_paths, tickers)
        
        html_search_tables = ""
        for file_path, df in search_results.items():
            file_name = os.path.basename(file_path)
            html_search_tables += f'<h2>Search Results from {file_name}</h2>'
            html_search_tables += '<div class="table-wrapper"><table class="styled-table"><thead><tr>'
            html_search_tables += ''.join([f'<th>{col}</th>' for col in df.columns])
            html_search_tables += '</tr></thead><tbody>'
            for index, row in df.iterrows():
                html_search_tables += '<tr>' + ''.join([f'<td>{cell}</td>' for cell in row]) + '</tr>'
            html_search_tables += '</tbody></table></div><br><br>'
        
        return render_template_string('''
            <html>
            <head>
                <title>Search Results</title>
                ''' + STYLE_BLOCK + '''
            </head>
            <body>
                <div class="container">
                    <h1>Search Results</h1>
                    {{ search_results|safe }}
                    <a href="/" class="btn btn-secondary">Search Again</a>
                </div>
            </body>
            </html>
        ''', search_results=html_search_tables)
    
    return '''
        <html>
        <head>
            <title>Search for Tickers</title>
            ''' + STYLE_BLOCK + '''
        </head>
        <body>
            <div class="container">
                <h1>Search for Tickers</h1>
                <form method="post">
                    <label for="tickers">Enter tickers (comma separated):</label>
                    <input type="text" id="tickers" name="tickers" required placeholder="e.g. AAPL, MSFT">
                    <input type="submit" value="Search">
                </form>
                <div style="display: flex; gap: 10px; justify-content: center; margin-top: 20px;">
                    <form method="get" action="/conventional_average">
                        <input type="submit" value="View Conventional Top Performers" class="btn btn-secondary">
                    </form>
                    <form method="get" action="/trendy_average">
                        <input type="submit" value="View Spicy Top Performers" class="btn btn-spicy">
                    </form>
                </div>
            </div>
        </body>
        </html>
    '''

@app.route('/conventional_average')
def conventional_average():
    file_path = 'Top Performing Companies by Ratios.csv'
    html_table = read_and_format_file(file_path)
    return render_template_string('''
        <html>
        <head>
            <title>Conventional Average Top Performers</title>
            ''' + STYLE_BLOCK + '''
        </head>
        <body>
            <div class="container">
                <h1>Conventional Average Top Performers</h1>
                {{ table|safe }}
                <a href="/" class="btn btn-secondary">Back to Search</a>
            </div>
        </body>
        </html>
    ''', table=html_table)

@app.route('/trendy_average')
def trendy_average():
    file_path = 'Top Performing Companies by Spicy Ratios.csv'
    html_table = read_and_format_file(file_path)
    return render_template_string('''
        <html>
        <head>
            <title>Spicy Average Top Performers</title>
            ''' + STYLE_BLOCK + '''
        </head>
        <body>
            <div class="container">
                <h1>Spicy Average Top Performers</h1>
                {{ table|safe }}
                <a href="/" class="btn btn-secondary">Back to Search</a>
            </div>
        </body>
        </html>
    ''', table=html_table)

if __name__ == '__main__':
    app.run(debug=True)
