import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd

df = pd.read_csv('/Users/sahajsomani1/Desktop/DSC 383/KOAA/final_dataset.csv')
df['year_month'] = pd.to_datetime(df['year_month'])

app = dash.Dash()


# Creating list of all categories
categories = ['Arts-Participate', 'Arts-Watch', 'Arts-Watch:Music/Concert', 'Arts-Watch:Dramatic arts', 'Arts-Visual', 'Outdoor-general', 'STEM',
            'Active - Participatory:Exercise', 'Active - Participatory:Sports', 'Academic', 'Special needs', 'Preschool', 'Other']

# Creating a dictionary of the dropdown options
regions = ['Northeast', 'Texas', 'Mountain', 'Southeast', 'Midwest', 'Canada']
options = []
for region in regions:
    options.append({'label':region, 'value':region})


app.layout = html.Div([
    dcc.Graph(id='graph'),
    dcc.Dropdown(id='region-picker',options=options,value='Northeast')
])

@app.callback(Output('graph', 'figure'),
              [Input('region-picker', 'value')])
def update_figure(region):
    filtered_df = df[(df[region] > 0) & (df['year_month'].dt.year >= 2015)] # Filtering based on region and post 2015
    main = filtered_df.groupby(filtered_df['year_month'].dt.month).mean()
    traces = []

    for category in categories:
        traces.append(go.Scatter(
            x=main.index,
            y=(main[category] - main[category].mean()),
            mode='lines',
            name=category
        ))

    return {
        'data': traces,
        'layout': go.Layout(
            title=region+': Seasonality',
            xaxis={'title': 'Month'},
            yaxis={'title': 'Popularity'},
            hovermode='closest',
            height=700
        )
    }

if __name__ == '__main__':
    app.run_server()
