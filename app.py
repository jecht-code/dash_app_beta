import dash
from dash import html, dcc, dash_table
import pandas as pd
import numpy as np
from dash.dependencies import Input, Output, State
import os

# Initialize the Dash app
app = dash.Dash(__name__)

# Load the Excel file
try:
    df = pd.read_excel('Catalog_File.xlsx')
    # Replace NaN values with empty strings
    df = df.fillna('')
except:
    # If Excel file doesn't exist or is empty, create a new DataFrame with the correct columns
    df = pd.DataFrame(columns=['Division', 'Brand', 'Category', 'Franchise', 'SubFranchise', 'ParentTag', 'Activity'])

# Store the original data
original_data = df.to_dict('records')

# Define the app layout
app.layout = html.Div([
    html.H1('Catalog Management System', style={'textAlign': 'center'}),
    
    # Filter container
    html.Div([
        html.Label('Filter by Brand:', style={'marginRight': '10px'}),
        dcc.Dropdown(
            id='brand-filter',
            options=[{'label': 'All Brands', 'value': 'All'}] + 
                    [{'label': brand, 'value': brand} for brand in sorted(df['Brand'].unique()) if brand],
            value='All',
            style={'width': '200px', 'display': 'inline-block'}
        )
    ], style={'textAlign': 'center', 'margin': '20px'}),
    
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
            data=original_data,
            editable=True,
            row_deletable=True,
            filter_action='none',
            sort_action='none',
            dropdown={
                'Activity': {
                    'options': [
                        {'label': 'Active', 'value': 'Active'},
                        {'label': 'Non-Active', 'value': 'Non-Active'}
                    ]
                }
            },
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
    html.Div(id='status-message', style={'textAlign': 'center', 'margin': '20px'}),
    
    # Store for keeping track of data
    dcc.Store(id='store-data', data=original_data),
    
    # Store for keeping mapping between filtered rows and original data
    dcc.Store(id='row-mapping', data=[]),
    
    # Store the filtered brand
    dcc.Store(id='filtered-brand', data='All')
])

# Callback to update brand filter options
@app.callback(
    Output('brand-filter', 'options'),
    Input('store-data', 'data')
)
def update_brand_options(stored_data):
    # Get unique brands from current data
    brands = sorted(set(row['Brand'] for row in stored_data if row.get('Brand', '').strip()))
    return [{'label': 'All Brands', 'value': 'All'}] + [{'label': brand, 'value': brand} for brand in brands]

# Store the current filter
@app.callback(
    Output('filtered-brand', 'data'),
    Input('brand-filter', 'value')
)
def store_filter(value):
    return value

# Callback to update data based on filtering
@app.callback(
    [Output('datatable', 'data'),
     Output('row-mapping', 'data')],
    Input('brand-filter', 'value'),
    State('store-data', 'data'),
    prevent_initial_call=True
)
def filter_data(selected_brand, stored_data):
    if selected_brand and selected_brand != 'All':
        filtered_data = []
        row_mapping = []  # Maps filtered rows to original data indices
        
        for i, row in enumerate(stored_data):
            if row.get('Brand', '').strip() == selected_brand.strip():
                filtered_data.append(row)
                row_mapping.append(i)
                
        return filtered_data, row_mapping
    
    # For All view, just use all rows and 1:1 mapping
    return stored_data, list(range(len(stored_data)))

# Callback to update data based on edits
@app.callback(
    Output('store-data', 'data', allow_duplicate=True),
    Input('datatable', 'data_timestamp'),
    [State('datatable', 'data'),
     State('store-data', 'data'),
     State('row-mapping', 'data'),
     State('filtered-brand', 'data')],
    prevent_initial_call=True
)
def update_store_on_edit(timestamp, table_data, stored_data, row_mapping, filtered_brand):
    if filtered_brand == 'All':
        # In "All" view, just use the table data directly
        return table_data
    else:
        # In filtered view, update only the mapped rows
        for i, filtered_row in enumerate(table_data):
            if i < len(row_mapping):
                original_idx = row_mapping[i]
                if original_idx < len(stored_data):
                    stored_data[original_idx] = filtered_row
        
        return stored_data

# Callback for adding new rows
@app.callback(
    [Output('datatable', 'data', allow_duplicate=True),
     Output('store-data', 'data', allow_duplicate=True),
     Output('row-mapping', 'data', allow_duplicate=True)],
    Input('add-row-button', 'n_clicks'),
    [State('datatable', 'data'),
     State('datatable', 'columns'),
     State('filtered-brand', 'data'),
     State('store-data', 'data'),
     State('row-mapping', 'data')],
    prevent_initial_call=True
)
def add_row(n_clicks, data, columns, selected_brand, stored_data, row_mapping):
    if n_clicks > 0:
        new_row = {c['id']: '' for c in columns}
        new_row['Activity'] = 'Non-Active'
        
        # Set the brand to the current filter if we're filtered
        if selected_brand != 'All':
            new_row['Brand'] = selected_brand
        
        # Add to the main data
        stored_data.append(new_row)
        
        # Update the view based on current filter
        if selected_brand == 'All' or (selected_brand != 'All' and new_row['Brand'] == selected_brand):
            data.append(new_row)
            row_mapping.append(len(stored_data) - 1)
            
    return data, stored_data, row_mapping

# Callback to handle row deletion
@app.callback(
    Output('store-data', 'data', allow_duplicate=True),
    Input('datatable', 'data'),
    [State('row-mapping', 'data'),
     State('store-data', 'data'),
     State('filtered-brand', 'data')],
    prevent_initial_call=True
)
def handle_deletion(table_data, row_mapping, stored_data, filtered_brand):
    # In filtered view, use row_mapping to determine which rows to keep
    if filtered_brand != 'All':
        # Get the IDs of rows displayed in the filtered view
        filtered_ids = set()
        for i, row in enumerate(table_data):
            filtered_ids.add(tuple(row.get(col, '') for col in row))
        
        # Get the original rows that correspond to filtered view
        filtered_rows = [stored_data[idx] for idx in row_mapping if idx < len(stored_data)]
        
        # Find which rows are missing in the filtered view
        deleted_indices = []
        for i, row in enumerate(filtered_rows):
            row_id = tuple(row.get(col, '') for col in row)
            if row_id not in filtered_ids and i < len(row_mapping):
                deleted_indices.append(row_mapping[i])
        
        # Create a new stored_data with deleted rows removed
        stored_data = [row for i, row in enumerate(stored_data) if i not in deleted_indices]
    else:
        # In "All" view, just use table_data directly
        stored_data = table_data
    
    return stored_data

# Callback to save changes
@app.callback(
    Output('status-message', 'children'),
    Input('save-button', 'n_clicks'),
    State('store-data', 'data'),
    prevent_initial_call=True
)
def save_changes(n_clicks, data):
    if n_clicks > 0:
        try:
            df = pd.DataFrame(data)
            df.to_excel('Catalog_File.xlsx', index=False)
            return html.Div('Changes saved successfully!', style={'color': 'green'})
        except Exception as e:
            return html.Div(f'Error saving changes: {str(e)}', style={'color': 'red'})
    return ''

if __name__ == '__main__':
    app.run(debug=True)