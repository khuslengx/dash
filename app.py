import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px


df = pd.read_csv('sales_data.csv', encoding='ISO-8859-1')

# Convert ORDERDATE to datetime format
df['ORDERDATE'] = pd.to_datetime(df['ORDERDATE'], errors='coerce')

# Initialize the Dash app
app = dash.Dash(__name__)
app.title = "Борлуулалтын мэдээллийн самбар"

# App layout
app.layout = html.Div(children=[
    html.H1("Борлуулалтын мэдээллийн самбар", style={'text-align': 'center'}),

    # Dropdown for country selection
    html.Div([
        html.Label("Улсыг сонгоно уу:"),
        dcc.Dropdown(
            id="country-dropdown",
            options=[{'label': country, 'value': country} for country in df['COUNTRY'].unique()],
            value=df['COUNTRY'].unique()[0]
        ),
    ], style={'width': '48%', 'display': 'inline-block'}),

    
    dcc.Graph(id="deal-size-graph"),
    dcc.Graph(id="deal-size-pie-chart"),
])

@app.callback(
    Output('deal-size-graph', 'figure'),
    Input('country-dropdown', 'value')
)
def update_deal_size_graph(selected_country):
    filtered_df = df[df['COUNTRY'] == selected_country]
    deal_size_data = filtered_df.groupby('DEALSIZE').sum(numeric_only=True).reset_index()
    fig = px.bar(deal_size_data, x='DEALSIZE', y='SALES',
                 title=f"Total Sales by Deal Size in {selected_country}",
                 labels={'DEALSIZE': 'Deal Size', 'SALES': 'Total Sales'})
    fig.update_layout(xaxis_title='Deal Size', yaxis_title='Total Sales')
    return fig

@app.callback(
    Output('deal-size-pie-chart', 'figure'),
    Input('country-dropdown', 'value')
)
def update_deal_size_pie_chart(selected_country):
    filtered_df = df[df['COUNTRY'] == selected_country]
    deal_size_data = filtered_df.groupby('DEALSIZE').sum(numeric_only=True).reset_index()
    fig = px.pie(deal_size_data, names='DEALSIZE', values='SALES',
                  title=f"Sales Distribution by Deal Size in {selected_country}")
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
