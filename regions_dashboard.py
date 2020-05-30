import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd

df = pd.read_csv('/Users/sahajsomani1/Desktop/DSC 383/KOAA/final_dataset.csv')

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
    filtered_df = df[df[region] > 0]  # Filtering for region
    main = filtered_df.groupby('year_month').sum()
    traces = []

    for category in categories:
        traces.append(go.Scatter(
            x=main.index[13:],
            y=(main[category]/main['pageviews']).rolling(13).mean()[13:],
            mode='lines',
            name=category
        ))

    return {
        'data': traces,
        'layout': go.Layout(
            title=region+': Popularity of Each Category Over Time',
            xaxis={'title': 'Year'},
            yaxis={'title': 'Proportional Pageviews'},
            hovermode='closest',
            height=700
        )
    }

if __name__ == '__main__':
    app.run_server()
