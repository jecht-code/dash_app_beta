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
            columns=[
                {"name": i, "id": i, "editable": True} 
                if i != 'Activity' 
                else {
                    "name": i, 
                    "id": i, 
                    "presentation": "dropdown"
                } 
                for i in df.columns
            ],
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
            style_data_conditional=[
                {
                    'if': {
                        'filter_query': '{Activity} eq "Active"',
                        'column_id': 'Activity'
                    },
                    'backgroundColor': '#90EE90',  # Light green
                    'color': 'black'
                },
                {
                    'if': {
                        'filter_query': '{Activity} eq "Non-Active"',
                        'column_id': 'Activity'
                    },
                    'backgroundColor': '#FFB6C1',  # Light pink
                    'color': 'black'
                }
            ],
            dropdown={
                'Activity': {
                    'options': [
                        {'label': 'Active', 'value': 'Active'},
                        {'label': 'Non-Active', 'value': 'Non-Active'}
                    ]
                }
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

# Combined callback for both adding rows and updating activity
@app.callback(
    Output('datatable', 'data'),
    Input('add-row-button', 'n_clicks'),
    Input('datatable', 'data_timestamp'),
    State('datatable', 'data'),
    State('datatable', 'columns'),
    State('datatable', 'active_cell'),
    prevent_initial_call=True
)
def update_table(add_clicks, timestamp, data, columns, active_cell):
    ctx = dash.callback_context
    if not ctx.triggered:
        return data
    
    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if trigger_id == 'add-row-button':
        if add_clicks > 0:
            new_row = {c['id']: '' for c in columns}
            new_row['Activity'] = 'Non-Active'  # Default to Non-Active for new rows
            data.append(new_row)
    elif trigger_id == 'datatable' and active_cell and active_cell['column_id'] == 'Activity':
        row = active_cell['row']
        current_value = data[row]['Activity']
        data[row]['Activity'] = 'Active' if current_value == 'Non-Active' else 'Non-Active'
    
    return data

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