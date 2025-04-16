import dash
from dash import html, dcc, dash_table
import pandas as pd
from dash.dependencies import Input, Output, State
import os

# Initialize the Dash app
app = dash.Dash(__name__)

# Load the CSV file
df = pd.read_csv('Catalog_File.csv')

# Define the app layout
app.layout = html.Div([
    html.H1('Catalog Management System', style={'textAlign': 'center'}),
    
    # Container for the table with centered styling
    html.Div([
        # Data table
        dash_table.DataTable(
            id='datatable',
            columns=[{"name": i, "id": i, "editable": True} for i in df.columns],
            data=df.to_dict('records'),
            editable=True,
            row_deletable=True,
            style_table={
                'overflowX': 'auto',
                'maxWidth': '80%',
                'margin': '0 auto',
                'border': 'thin lightgrey solid'
            },
            style_cell={
                'minWidth': '100px', 
                'width': '150px', 
                'maxWidth': '180px',
                'whiteSpace': 'normal',
                'textAlign': 'left',
                'padding': '10px'
            },
            style_header={
                'backgroundColor': 'rgb(230, 230, 230)',
                'fontWeight': 'bold',
                'textAlign': 'center'
            },
            style_data={
                'whiteSpace': 'normal',
                'height': 'auto'
            },
            page_size=10  # Show 10 rows per page
        ),
    ], style={'margin': '20px'}),
    
    # Button container with centered styling
    html.Div([
        html.Button('Add Row', id='add-row-button', n_clicks=0, 
                   style={'margin': '10px', 'padding': '10px 20px'}),
        html.Button('Save Changes', id='save-button', n_clicks=0,
                   style={'margin': '10px', 'padding': '10px 20px'})
    ], style={'textAlign': 'center', 'margin': '20px'}),
    
    # Status message with centered styling
    html.Div(id='status-message', style={'textAlign': 'center', 'margin': '20px'})
])

# Callback to add new row
@app.callback(
    Output('datatable', 'data'),
    Input('add-row-button', 'n_clicks'),
    State('datatable', 'data'),
    State('datatable', 'columns')
)
def add_row(n_clicks, rows, columns):
    if n_clicks > 0:
        rows.append({c['id']: '' for c in columns})
    return rows

# Callback to save changes
@app.callback(
    Output('status-message', 'children'),
    Input('save-button', 'n_clicks'),
    State('datatable', 'data')
)
def save_changes(n_clicks, data):
    if n_clicks > 0:
        try:
            # Convert the data back to a DataFrame
            df = pd.DataFrame(data)
            # Save to CSV
            df.to_csv('Catalog_File.csv', index=False)
            return html.Div('Changes saved successfully!', style={'color': 'green'})
        except Exception as e:
            return html.Div(f'Error saving changes: {str(e)}', style={'color': 'red'})
    return ''

if __name__ == '__main__':
    app.run(debug=True) 