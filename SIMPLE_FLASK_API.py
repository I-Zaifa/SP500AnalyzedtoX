# Written entirely-mostly By Mssr.GPT
# I had to go over 15 iterations and such. Mercy me!

from flask import Flask, request, render_template_string
import pandas as pd
import os

app = Flask(__name__)

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
            html_table = '<table class="styled-table"><thead><tr>'
            html_table += ''.join([f'<th>{col}</th>' for col in df.columns])
            html_table += '</tr></thead><tbody>'
            for index, row in df.iterrows():
                html_table += '<tr>' + ''.join([f'<td>{cell}</td>' for cell in row]) + '</tr>'
            html_table += '</tbody></table><br><br>'
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
        
        # File paths for search
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
            html_search_tables += '<table class="styled-table"><thead><tr>'
            html_search_tables += ''.join([f'<th>{col}</th>' for col in df.columns])
            html_search_tables += '</tr></thead><tbody>'
            for index, row in df.iterrows():
                html_search_tables += '<tr>' + ''.join([f'<td>{cell}</td>' for cell in row]) + '</tr>'
            html_search_tables += '</tbody></table><br><br>'
        
        return render_template_string('''
            <html>
            <head>
                <title>Search Results</title>
                <style>
                    body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f8f9fa; color: #333; margin: 20px; }
                    h1 { color: #2c3e50; font-size: 1.5rem; margin-top: 30px; }
                    h2 { color: #34495e; font-size: 1.2rem; margin-top: 20px; border-bottom: 2px solid #ddd; padding-bottom: 5px; }
                    .styled-table { border-collapse: collapse; margin: 10px 0; font-size: 0.85rem; font-family: sans-serif; min-width: 100%; box-shadow: 0 0 20px rgba(0, 0, 0, 0.05); background-color: white; }
                    .styled-table thead tr { background-color: #009879; color: #ffffff; text-align: left; }
                    .styled-table th, .styled-table td { padding: 8px 10px; border-bottom: 1px solid #dddddd; }
                    .styled-table tbody tr { border-bottom: 1px solid #dddddd; }
                    .styled-table tbody tr:nth-of-type(even) { background-color: #f3f3f3; }
                    .styled-table tbody tr:last-of-type { border-bottom: 2px solid #009879; }
                    a { display: inline-block; margin-top: 20px; padding: 10px 15px; background-color: #009879; color: white; text-decoration: none; border-radius: 4px; font-weight: bold; }
                    a:hover { background-color: #007f67; }
                </style>
            </head>
            <body>
                <h1>Search Results</h1>
                {{ search_results|safe }}
                <a href="/">Search Again</a>
            </body>
            </html>
        ''', search_results=html_search_tables)
    
    return '''
        <html>
        <head>
            <title>Search for Tickers</title>
            <style>
                body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f8f9fa; display: flex; flex-direction: column; align-items: center; padding-top: 50px; }
                h1 { color: #2c3e50; }
                form { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 20px; width: 300px; display: flex; flex-direction: column; gap: 10px; }
                label { font-weight: bold; margin-bottom: 5px; color: #555; }
                input[type="text"] { padding: 10px; border: 1px solid #ccc; border-radius: 4px; }
                input[type="submit"] { padding: 10px; background-color: #009879; color: white; border: none; border-radius: 4px; cursor: pointer; font-weight: bold; transition: background 0.3s; }
                input[type="submit"]:hover { background-color: #007f67; }
            </style>
        </head>
        <body>
            <h1>Search for Tickers</h1>
            <form method="post">
                <label for="tickers">Enter tickers (comma separated):</label>
                <input type="text" id="tickers" name="tickers" required placeholder="e.g. AAPL, MSFT">
                <input type="submit" value="Search">
            </form>
            <form method="get" action="/conventional_average">
                <label>Conventional Analysis</label>
                <input type="submit" value="View Conventional Top Performers">
            </form>
            <form method="get" action="/trendy_average">
                <label>Spicy Analysis</label>
                <input type="submit" value="View Spicy Top Performers">
            </form>
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
            <style>
                body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f8f9fa; color: #333; margin: 20px; }
                h1 { color: #2c3e50; font-size: 1.5rem; }
                .styled-table { border-collapse: collapse; margin: 25px 0; font-size: 0.85rem; font-family: sans-serif; min-width: 100%; box-shadow: 0 0 20px rgba(0, 0, 0, 0.15); background-color: white; }
                .styled-table thead tr { background-color: #009879; color: #ffffff; text-align: left; }
                .styled-table th, .styled-table td { padding: 10px 12px; border-bottom: 1px solid #dddddd; }
                .styled-table tbody tr { border-bottom: 1px solid #dddddd; }
                .styled-table tbody tr:nth-of-type(even) { background-color: #f3f3f3; }
                .styled-table tbody tr:last-of-type { border-bottom: 2px solid #009879; }
                a { display: inline-block; margin-top: 20px; padding: 10px 15px; background-color: #2c3e50; color: white; text-decoration: none; border-radius: 4px; font-weight: bold; }
                a:hover { background-color: #1a252f; }
            </style>
        </head>
        <body>
            <h1>Conventional Average Top Performers</h1>
            {{ table|safe }}
            <a href="/">Back to Search</a>
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
            <style>
                body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f8f9fa; color: #333; margin: 20px; }
                h1 { color: #2c3e50; font-size: 1.5rem; }
                .styled-table { border-collapse: collapse; margin: 25px 0; font-size: 0.85rem; font-family: sans-serif; min-width: 100%; box-shadow: 0 0 20px rgba(0, 0, 0, 0.15); background-color: white; }
                .styled-table thead tr { background-color: #d35400; color: #ffffff; text-align: left; }
                .styled-table th, .styled-table td { padding: 10px 12px; border-bottom: 1px solid #dddddd; }
                .styled-table tbody tr { border-bottom: 1px solid #dddddd; }
                .styled-table tbody tr:nth-of-type(even) { background-color: #f3f3f3; }
                .styled-table tbody tr:last-of-type { border-bottom: 2px solid #d35400; }
                a { display: inline-block; margin-top: 20px; padding: 10px 15px; background-color: #2c3e50; color: white; text-decoration: none; border-radius: 4px; font-weight: bold; }
                a:hover { background-color: #1a252f; }
            </style>
        </head>
        <body>
            <h1>Spicy Average Top Performers</h1>
            {{ table|safe }}
            <a href="/">Back to Search</a>
        </body>
        </html>
    ''', table=html_table)

if __name__ == '__main__':
    app.run(debug=True)
