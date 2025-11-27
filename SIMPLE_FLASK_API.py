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
                print(f"File not found: {file_path}")
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
    return results

def read_and_format_file(file_path):
    try:
        if os.path.isfile(file_path):
            df = pd.read_csv(file_path)
            html_table = '<table border="1" style="width:100%; border-collapse:collapse;"><thead><tr>'
            html_table += ''.join([f'<th>{col}</th>' for col in df.columns])
            html_table += '</tr></thead><tbody>'
            for index, row in df.iterrows():
                html_table += '<tr>' + ''.join([f'<td>{cell}</td>' for cell in row]) + '</tr>'
            html_table += '</tbody></table><br><br>'
            return html_table
        else:
            return f"<p>File not found: {file_path}</p>"
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return f"<p>Error reading {file_path}</p>"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        raw = request.form.get('tickers') or ''
        tickers = [t.strip() for t in raw.split(',') if t.strip()]
        
        # File paths for search
        search_file_paths = [
            'All_Ratios/ratioAverages/average.csv',
            'All_Ratios/Risk_analysison_Ratios/analyzed_metrics_individual_r2.csv',
            'All_Stock/dividends_etc/dividends_analysis.csv',
            'All_Stock/stock_metrics/stocks_analyzed.csv',
        ]
        
        search_results = search_tickers_in_files(search_file_paths, tickers)
        
        html_search_tables = ""
        for file_path, df in search_results.items():
            file_name = os.path.basename(file_path)
            html_search_tables += f'<h2>Search Results from {file_name}</h2>'
            html_search_tables += '<table border="1" style="width:100%; border-collapse:collapse;"><thead><tr>'
            html_search_tables += ''.join([f'<th>{col}</th>' for col in df.columns])
            html_search_tables += '</tr></thead><tbody>'
            for index, row in df.iterrows():
                html_search_tables += '<tr>' + ''.join([f'<td>{cell}</td>' for cell in row]) + '</tr>'
            html_search_tables += '</tbody></table><br><br>'
        

        conventional_average_file_path = 'All_Ratios/ratioAverages/Top Performing Companies by Ratios.csv'
        trendy_average_file_path = 'Top Performing Companies by Spicy Ratios.csv'
        
        conventional_average_html = read_and_format_file(conventional_average_file_path)
        trendy_average_html = read_and_format_file(trendy_average_file_path)
        
        return render_template_string('''
            <html>
            <head>
                <title>Search Results</title>
                <style>
                    table, th, td {
                        border: 1px solid black;
                        border-collapse: collapse;
                    }
                    th, td {
                        padding: 8px;
                        text-align: left;
                    }
                    th {
                        background-color: #f2f2f2;
                    }
                </style>
            </head>
            <body>
                <h1>Search Results</h1>
                {{ search_results|safe }}
                <h1>Conventional Average Top Performers</h1>
                {{ conventional_average|safe }}
                <h1>Spicy Average Top Performers</h1>
                {{ trendy_average|safe }}
                <a href="/">Search Again</a>
            </body>
            </html>
        ''', search_results=html_search_tables, conventional_average=conventional_average_html, trendy_average=trendy_average_html)
    
    return '''
        <html>
        <head>
            <title>Search for Tickers</title>
        </head>
        <body>
            <h1>Search for Tickers</h1>
            <form method="post">
                <label for="tickers">Enter the tickers to search for (separated by commas):</label><br>
                <input type="text" id="tickers" name="tickers" required><br><br>
                <input type="submit" value="Search">
            </form>
            <h1>Conventional Average Top Performers</h1>
            <form method="get" action="/conventional_average">
                <input type="submit" value="View Conventional Average Top Performers">
            </form>
            <h1>Spicy Average Top Performers</h1>
            <form method="get" action="/trendy_average">
                <input type="submit" value="View Spicy Average Top Performers">
            </form>
        </body>
        </html>
    '''

@app.route('/conventional_average')
def conventional_average():
    file_path = 'All_Ratios/ratioAverages/Top Performing Companies by Ratios.csv'
    html_table = read_and_format_file(file_path)
    return render_template_string('''
        <html>
        <head>
            <title>Conventional Average Top Performers</title>
            <style>
                table, th, td {
                    border: 1px solid black;
                    border-collapse: collapse;
                }
                th, td {
                    padding: 8px;
                    text-align: left;
                }
                th {
                    background-color: #f2f2f2;
                }
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
                table, th, td {
                    border: 1px solid black;
                    border-collapse: collapse;
                }
                th, td {
                    padding: 8px;
                    text-align: left;
                }
                th {
                    background-color: #f2f2f2;
                }
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
