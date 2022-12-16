from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objects as go
from skimage import io
import os
from plotly.figure_factory import create_dendrogram
import base64
from upsetplot import generate_counts
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
from upsetplot import from_memberships
from upsetplot import plot
from itertools import compress
import itertools
from numbers import Number
from plotly import exceptions, optional_imports
import plotly.colors as clrs
from plotly.graph_objs import graph_objs
from plotly.subplots import make_subplots

app = Dash(__name__)

# Load the CSV file into a DataFrame
df = pd.read_csv('ATUS_withCombinedTelephonecalls_and_incomelevelperannum.csv')

app.layout = html.Div([
    html.H2('Visualization of ATUS Dataset', style={'text-align':'center', 'font-family': 'Sans-serif'}),
    html.P('Choose the number of dimensions you want to visualize:', style={'font-family': 'Sans-serif'}),
    dcc.RadioItems(
        id="radio",
        options=['1 Dimension(s)', '2 Dimension(s)','3 Dimension(s)', '4 Dimension(s)', '5 Dimension(s)'],
        value="1 Dimension(s)",
        style={'font-family': 'Sans-serif'}
    ),
    html.Br(),
    html.Div(id='radio-output')
])


@app.callback(
    Output("radio-output", "children"),
    Input("radio", "value"))

def update_output(value):
    if value == '1 Dimension(s)':
        return html.Div([
            html.P("Choose a Distribution:", style={'font-family': 'Sans-serif'}),
            dcc.Dropdown(
                id="dist-dropdown",
                options=["Distribution of males and females", "Distribution of metro and non-metro people", "Distribution of people in different age groups",
                         "Distribution of people in different income levels", "Distribution of people based on their time spent on leisure"],
                value="Distribution of males and females",
                style={'font-family': 'Sans-serif'},
                clearable=False,
            ),
            dcc.Graph(id="graph")
        ])
    elif value == '2 Dimension(s)':
        return html.Div([
            html.P("Choose a Distribution:", style={'font-family': 'Sans-serif'}),
            dcc.Dropdown(
                id="dist-dropdown-two",
                options=["Distribution of males & females in metro & non-metro cities", "Distribution of males & females in different age groups",
                         "Distribution of males & females in different income levels", "Distribution of males & females based on their time spent in leisure",
                         "Distribution of metro and non-metro people in different age groups", "Distribution of metro and non-metro people in different income levels",
                         "Distribution of metro and non-metro people based on their time spent in leisure",
                         "Distribution of people in different income levels based on their age groups",
                         "Distribution of people based on their time spent on leisure in different income levels",
                         "Distribution of people based on their time spent on leisure in different age groups"],
                value="Distribution of males & females in metro & non-metro cities",
                style={'font-family': 'Sans-serif'},
                clearable=False,
            ),
            html.Br(),
            html.P("Choose the type of visualization(s):", style={'font-family': 'Sans-serif'}),
            dcc.RadioItems(
                id="radiotwo",
                options=["Heatmap", "Adjacent bar chart"],
                value="Heatmap",
                style={'font-family': 'Sans-serif'}
            ),
            dcc.Graph(id="twodim", style={'display': 'inline-block', 'width': '49%'})
        ])
    elif value == '3 Dimension(s)':
        return html.Div([
            html.P("Choose the visualization type to visualize 3-Dimensional data(Age groups, gender and city type)", style={'font-family': 'Sans-serif'}),
            dcc.RadioItems(
                id="radiothree",
                options=["Sankey Diagram", "Treemap"],
                value="Sankey Diagram",
                style={'font-family': 'Sans-serif'}
            ),
            html.P("Choose the number of bins for age (Only if you choose sankey diagram):", style={'font-family': 'Sans-serif'}),
            dcc.Dropdown(
                id="dropdownthree",
                options=['3', '4', '5'],
                value='3',
                style={'font-family': 'Sans-serif'},
                clearable=False,
            ),
            dcc.Graph(id="threedim")
        ])
    elif value == '4 Dimension(s)':
        return html.Div([
            html.P("Choose the visualization type to visualize 4-Dimensional data(Age groups, gender, income_bins, city type)",
                   style={'font-family': 'Sans-serif'}),
            dcc.RadioItems(
                id="radiofour",
                options=["Treemap", "Circular Packing", "Upset Plot"],
                value="Treemap",
                style={'font-family': 'Sans-serif'}
            ),
            dcc.Graph(id="fourdim"),
            html.Div(id="image")
        ])
    else:
        return html.Div([
            html.P("Heirarchy of clusters/bins in Dendrogram", style={'font-family': 'Sans-serif'}),
            dcc.RadioItems(
                id="radiofive",
                options=["Dendrogram"],
                value="Dendrogram",
                style={'font-family': 'Sans-serif'}
            ),
            dcc.Graph(id="fived")
            ])

@app.callback(
    Output("fived", "figure"),
    Input("radiofive", "value"),
    supress_callback_exceptions=True)

def dendo(value):
    X = np.array(
        [[5958], [1494], [4190], [933], [2370], [473], [3710], [876], [4072], [893], [4099], [694], [3932], [1563], [3706],
         [1091], [3393], [773], [1421], [328], [654], [118], [160], [25], [951], [215], [750], [155], [337], [58], [1065],
         [422], [736], [200], [314], [89], [3399], [1495], [3721], [1287], [3603], [973], [1433], [563], [3402], [1115],
         [6404], [1530], [1681], [1031], [2665], [1111], [4653], [1392], [763], [302], [801], [211], [375], [79], [339], [148],
         [778], [234], [660], [154], [430], [273], [676], [268], [555], [171]]
    )
    names = ["Female      Metro    Young        middle class       Upto 6 hours",
             "Female      Metro    Young        middle class  More than 6 hours",
             "Female      Metro    Young  upper-middle class       Upto 6 hours",
             "Female      Metro    Young  upper-middle class  More than 6 hours",
             "Female      Metro    Young             wealthy       Upto 6 hours",
             "Female      Metro    Young             wealthy  More than 6 hours",
             "Female      Metro    Adult        middle class       Upto 6 hours",
             "Female      Metro    Adult        middle class  More than 6 hours",
             "Female      Metro    Adult  upper-middle class       Upto 6 hours",
             "Female      Metro    Adult  upper-middle class  More than 6 hours",
             "Female      Metro    Adult             wealthy       Upto 6 hours",
             "Female      Metro    Adult             wealthy  More than 6 hours",
             "Female      Metro  Elderly        middle class       Upto 6 hours",
             "Female      Metro  Elderly        middle class  More than 6 hours",
             "Female      Metro  Elderly  upper-middle class       Upto 6 hours",
             "Female      Metro  Elderly  upper-middle class  More than 6 hours",
             "Female      Metro  Elderly             wealthy       Upto 6 hours",
             "Female      Metro  Elderly             wealthy  More than 6 hours",
             "Female  Non-metro    Young        middle class       Upto 6 hours",
             "Female  Non-metro    Young        middle class  More than 6 hours",
             "Female  Non-metro    Young  upper-middle class       Upto 6 hours",
             "Female  Non-metro    Young  upper-middle class  More than 6 hours",
             "Female  Non-metro    Young             wealthy       Upto 6 hours",
             "Female  Non-metro    Young             wealthy  More than 6 hours",
             "Female  Non-metro    Adult        middle class       Upto 6 hours",
             "Female  Non-metro    Adult        middle class  More than 6 hours",
             "Female  Non-metro    Adult  upper-middle class       Upto 6 hours",
             "Female  Non-metro    Adult  upper-middle class  More than 6 hours",
             "Female  Non-metro    Adult             wealthy       Upto 6 hours",
             "Female  Non-metro    Adult             wealthy  More than 6 hours",
             "Female  Non-metro  Elderly        middle class       Upto 6 hours",
             "Female  Non-metro  Elderly        middle class  More than 6 hours",
             "Female  Non-metro  Elderly  upper-middle class       Upto 6 hours",
             "Female  Non-metro  Elderly  upper-middle class  More than 6 hours",
             "Female  Non-metro  Elderly             wealthy       Upto 6 hours",
             "Female  Non-metro  Elderly             wealthy  More than 6 hours",
             "Male      Metro    Young        middle class       Upto 6 hours",
             "Male      Metro    Young        middle class  More than 6 hours",
             "Male      Metro    Young  upper-middle class       Upto 6 hours",
             "Male      Metro    Young  upper-middle class  More than 6 hours",
             "Male      Metro    Young             wealthy       Upto 6 hours",
             "Male      Metro    Young             wealthy  More than 6 hours",
             "Male      Metro    Adult        middle class       Upto 6 hours",
             "Male      Metro    Adult        middle class  More than 6 hours",
             "Male      Metro    Adult  upper-middle class       Upto 6 hours",
             "Male      Metro    Adult  upper-middle class  More than 6 hours",
             "Male      Metro    Adult             wealthy       Upto 6 hours",
             "Male      Metro    Adult             wealthy  More than 6 hours",
             "Male      Metro  Elderly        middle class       Upto 6 hours",
             "Male      Metro  Elderly        middle class  More than 6 hours",
             "Male      Metro  Elderly  upper-middle class       Upto 6 hours",
             "Male      Metro  Elderly  upper-middle class  More than 6 hours",
             "Male      Metro  Elderly             wealthy       Upto 6 hours",
             "Male      Metro  Elderly             wealthy  More than 6 hours",
             "Male  Non-metro    Young        middle class       Upto 6 hours",
             "Male  Non-metro    Young        middle class  More than 6 hours",
             "Male  Non-metro    Young  upper-middle class       Upto 6 hours",
             "Male  Non-metro    Young  upper-middle class  More than 6 hours",
             "Male  Non-metro    Young             wealthy       Upto 6 hours",
             "Male  Non-metro    Young             wealthy  More than 6 hours",
             "Male  Non-metro    Adult        middle class       Upto 6 hours",
             "Male  Non-metro    Adult        middle class  More than 6 hours",
             "Male  Non-metro    Adult  upper-middle class       Upto 6 hours",
             "Male  Non-metro    Adult  upper-middle class  More than 6 hours",
             "Male  Non-metro    Adult             wealthy       Upto 6 hours",
             "Male  Non-metro    Adult             wealthy  More than 6 hours",
             "Male  Non-metro  Elderly        middle class       Upto 6 hours",
             "Male  Non-metro  Elderly        middle class  More than 6 hours",
             "Male  Non-metro  Elderly  upper-middle class       Upto 6 hours",
             "Male  Non-metro  Elderly  upper-middle class  More than 6 hours",
             "Male  Non-metro  Elderly             wealthy       Upto 6 hours",
             "Male  Non-metro  Elderly             wealthy  More than 6 hours"]

    dendro = create_dendrogram(X, orientation='bottom', labels=names)
    dendro.update_layout({'width': 1500, 'height': 1000})

    return dendro


@app.callback(
    [Output("fourdim", "figure"), Output("image", "children")],
    Input("radiofour", "value"),
    supress_callback_exceptions=True)

def fourGraphOne(radio_value):
    global df
    if radio_value == "Treemap":
        print("radio_value")
        df = df[(df['TRERNWA'] > 45000)]
        income_labels = ['lower-middle class', 'middle class', 'upper-middle class', 'wealthy']
        # equal depth binning
        df['income_bin'] = pd.qcut(df['TRERNWA'], q=4, precision=0, duplicates='drop', labels=income_labels)
        df_grouped = df.groupby(['TESEX', 'GTMETSTA', 'age_bin', 'income_bin'])
        df_counts = df_grouped.size().reset_index(name='count')
        fig = px.treemap(
            df_counts,                 # Specify the DataFrame to use for the treemap
            path=['TESEX', 'GTMETSTA', 'age_bin', 'income_bin'],  # Set the hierarchy of the treemap
            values='count',      # Set the values to be plotted
            title='Number of Females and males in each category',  # Set the title for the plot
        )
        fig.update_layout(width=1000, height=1000)
        return [fig, html.Div()]

    elif radio_value == "Circular Packing":
        fig = go.Figure()
        fig.update_layout(width=10, height=10)
        return [fig, html.Div([
            html.P("Choose gender:", style={'font-family': 'Sans-serif'}),
            dcc.Dropdown(
                id="dropdownfour",
                options=["Male", "Female"],
                value="Male",
                style={'font-family': 'Sans-serif'},
                clearable=False,
            ),
            dcc.Graph(id="fdim", style={'width': '500', 'height': '500'})
        ])]

    elif radio_value == "Upset Plot":
        img = io.imread('upset_plot.PNG')
        fig = px.imshow(img).update_layout(dragmode="drawclosedpath")
        fig.update_layout(width=1000, height=1000)
        return [fig, html.Div([html.P(" ")])]

@app.callback(
    Output("fdim", "figure"),
    Input("dropdownfour", "value"),
    supress_callback_exceptions=True)

def malegraph(value):
    if value == "Male":
        img = io.imread('male_selected.jpeg')
        fig = px.imshow(img).update_layout(dragmode="drawclosedpath")
        fig.update_layout(width=1000, height=1000)
        return fig
    elif value == "Female":
        img = io.imread('female_selected.jpeg')
        fig = px.imshow(img).update_layout(dragmode="drawclosedpath")
        fig.update_layout(width=1000, height=1000)
        return fig

@app.callback(
    Output("threedim", "figure"),
    [Input("radiothree", "value"),Input("dropdownthree", "value")],
    supress_callback_exceptions=True)

def threedgraph(radio_value, Age_bins):
    global df
    if radio_value == "Treemap":
        df_grouped = df.groupby(['TESEX', 'GTMETSTA', 'age_bin'])
        df_counts = df_grouped.size().reset_index(name='count')
        # Create the treemap using the go.Treemap function from the plotly.express module
        fig = px.treemap(
            df_counts,                 # Specify the DataFrame to use for the treemap
            path=['TESEX', 'GTMETSTA', 'age_bin'],  # Set the hierarchy of the treemap
            values='count',      # Set the values to be plotted
            title='Number of Females and males in each category',  # Set the title for the plot

        )
        # set the width and height of the treemap to 500 pixels
        fig.update_layout(width=1000, height=1000)
        return fig
    else:
        if Age_bins == '3':
            label = ["Male", "Female", "Metropolitan", "Non-Metropolitan", "Young", "Adult", "Elderly"]
            source = [0, 0, 1, 1, 2, 2, 2, 3, 3, 3]
            target = [2, 3, 2, 3, 4, 5, 6, 4, 5, 6]
            value = [73102, 14304, 91895, 18524, 56237, 57603, 51157, 9965, 10624, 12239]
        elif Age_bins == '4':
            label = ["Male", "Female", "Metropolitan", "Non-Metropolitan", "Young Adult", "Adult", "Middle Aged", "Elderly"]
            source = [0, 0, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3]
            target = [2, 3, 2, 3, 4, 5, 6, 7, 4, 5, 6, 7]
            value = [73102, 14304, 91895, 18524, 42900, 42748, 41023, 38326, 7748, 7211, 8492, 9377]
        elif Age_bins == '5':
            label = ["Metropolitan", "Non-Metropolitan", "Male", "Female", "Young", "Young Adult", "Adult", "Middle Aged", "Elderly"]
            source = [0, 0, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3]
            target = [2, 3, 2, 3, 4, 5, 6, 7, 8, 4, 5, 6, 7, 8]
            value = [73102, 14304, 91895, 18524, 27721, 45454, 40665, 32059, 19098, 5134, 7580, 7875, 7403, 4836]

        link = dict(source = source, target = target, value = value)

        node = dict(label=label, pad=35, thickness=10)
        data = go.Sankey(link = link, node = node)
        fig = go.Figure(data)
        fig.update_layout(
            hovermode = 'x',
            font = dict(size=10, color='white'),
            paper_bgcolor = '#51504f'
        )
        return fig

@app.callback(
    Output("twodim", "figure"),
    [Input("dist-dropdown-two", "value"), Input("radiotwo", "value")],
    suppress_callback_exceptions=True)

def graph_output(dropdown_value, radio_value):
    def radioOption(x, y):
        global df
        if radio_value == "Heatmap":
            if x == 'income_bin' or y == 'income_bin':
                df = df[(df['TRERNWA'] > 45000)]
                income_labels = ['middle class', 'upper-middle class', 'wealthy']
                df['income_bin'] = pd.qcut(df['TRERNWA'], q=3, precision=0, duplicates='drop', labels=income_labels)
            df_grouped = df.groupby([x, y])
            df_counts = df_grouped.size().reset_index(name='count')
            trace = go.Heatmap(
                x = df_counts[x],
                y = df_counts[y],
                z = df_counts['count'],
                type = 'heatmap',
                colorscale = 'Viridis'
            )
            data = [trace]
            fig = go.Figure(data=data)
            return fig
        elif radio_value == "Adjacent bar chart":
            #df = pd.read_csv('adjacentbar.csv')
            if x == 'income_bin' or y == 'income_bin':
                df = df[(df['TRERNWA'] > 45000)]
                income_labels = ['middle class', 'upper-middle class', 'wealthy']
                df['income_bin'] = pd.qcut(df['TRERNWA'], q=3, precision=0, duplicates='drop', labels=income_labels)
            df_grouped = df.groupby([x, y])
            df_counts = df_grouped.size().reset_index(name='count')
            fig = px.bar(df_counts, x=x, y='count',
                         color=y, barmode='group',
                         height=400)
            return fig




    if dropdown_value == "Distribution of males & females in metro & non-metro cities":
        return radioOption('TESEX', 'GTMETSTA')
    elif dropdown_value == "Distribution of males & females in different age groups":
        return radioOption('TESEX', 'age_bin')
    elif dropdown_value == "Distribution of males & females in different income levels":
        return radioOption('TESEX', 'income_bin')
    elif dropdown_value == "Distribution of males & females based on their time spent in leisure":
        return radioOption('TESEX', 'leisure_bin')
    elif dropdown_value == "Distribution of metro and non-metro people in different age groups":
        return radioOption('GTMETSTA', 'age_bin')
    elif dropdown_value == "Distribution of metro and non-metro people in different income levels":
        return radioOption('GTMETSTA', 'income_bin')
    elif dropdown_value == "Distribution of metro and non-metro people based on their time spent in leisure":
        return radioOption('GTMETSTA', 'leisure_bin')
    elif dropdown_value == "Distribution of people in different income levels based on their age groups":
        return radioOption('income_bin', 'age_bin')
    elif dropdown_value == "Distribution of people based on their time spent on leisure in different income levels":
        return radioOption('leisure_bin', 'income_bin')
    elif dropdown_value == "Distribution of people based on their time spent on leisure in different age groups":
        return radioOption('leisure_bin', 'age_bin')




@app.callback(
    Output("graph", "figure"),
    Input("dist-dropdown", "value"),
    suppress_callback_exceptions=True)

def dropdown_output(value):
    if value == "Distribution of males and females":
        # create a DataFrame with the data for the chart
        pf = pd.DataFrame({'Gender': ['Male', 'Female'], 'Population': [87406, 110419]})
        # create the bar chart using plotly.express.bar
        fig = px.bar(pf, x='Gender', y='Population', title='Population of Males and Females')
    elif value == "Distribution of metro and non-metro people":
        # create a DataFrame with the data for the chart
        pf = pd.DataFrame({'Type of City': ['Metro', 'Non-metro'], 'Population': [164997, 32828]})
        # create the bar chart using plotly.express.bar
        fig = px.bar(pf, x='Type of City', y='Population', title='Population of Metro and Non-metro People')
    elif value == "Distribution of people in different age groups":
        # create a DataFrame with the data for the chart
        pf = pd.DataFrame({'Age Groups': ['Young', 'Adult', 'Middle-Aged', 'Elderly'], 'Population': [50648, 49959, 49515, 47703]})
        # create the bar chart using plotly.express.bar
        fig = px.bar(pf, x='Age Groups', y='Population', title='Population of People in each Age Group')
    elif value == "Distribution of people in different income levels":
        # create a DataFrame with the data for the chart
        pf = pd.DataFrame({'Income Level': ['Middle Class', 'Upper Middle Class', 'Wealthy'], 'Population': [35822, 35951, 35692]})
        # create the bar chart using plotly.express.bar
        fig = px.bar(pf, x='Income Level', y='Population', title='Population of People in each Income level (>45000)')
    else:
        # create a DataFrame with the data for the chart
        pf = pd.DataFrame({'Time spent on Leisure': ['Up to 6 hours', 'More than 6 hours'], 'Population': [78156, 22737]})
        # create the bar chart using plotly.express.bar
        fig = px.bar(pf, x='Time spent on Leisure', y='Population', title='Population of People based on their time spent on Leisure')

    return fig


if __name__ == "__main__":
    app.run_server(debug=True)
