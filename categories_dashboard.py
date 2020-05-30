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
            'Active - Participatory:Exercise', 'Active - Participatory:Sports', 'Academic', 'Special needs', 'Preschool', 'Other', 'All']

regions = ['Northeast', 'Texas', 'Mountain', 'Southeast', 'Midwest', 'Canada']

# Creating a dictionary of the dropdown options
options = []
for category in categories:
    options.append({'label':category, 'value':category})


app.layout = html.Div([
    dcc.Graph(id='graph'),
    dcc.Dropdown(id='category-picker',options=options,value='Arts-Participate')
])

@app.callback(Output('graph', 'figure'),
              [Input('category-picker', 'value')])
def update_figure(category):
    filtered_df = df[df[category] > 0]  # Filtering for category

    for region in regions:
        filtered_df[region] = filtered_df[region]*filtered_df['pageviews']

    main = filtered_df.groupby('year_month').sum()
    traces = []

    for region in regions:
        if category == 'All':
            traces.append(go.Scatter(
                x=main.index[13:],
                y=((df[df[region] > 0].groupby('year_month').sum()['pageviews']/df.groupby('year_month').sum()['pageviews'])).rolling(13).mean()[13:],
                mode='lines',
                name=region
            ))
        else:
            traces.append(go.Scatter(
                x=main.index[13:],
                y=((main[region]/main['pageviews']) - (df[df[region] > 0].groupby('year_month').sum()['pageviews']/df.groupby('year_month').sum()['pageviews'])).rolling(13).mean()[13:],
                mode='lines',
                name=region
            ))

    return {
        'data': traces,
        'layout': go.Layout(
            title=category+' --> Popularity of Each Region Over Time',
            xaxis={'title': 'Year'},
            yaxis={'title': 'Proportional Pageviews'},
            hovermode='closest',
            height=700
        )
    }

if __name__ == '__main__':
    app.run_server()
