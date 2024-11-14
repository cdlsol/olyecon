import plotly.express as px
from shiny import reactive, App
from shiny.express import render, input, ui
from shiny.express import app as express_app
from shiny.ui import page_navbar
from shinywidgets import render_plotly
from functools import partial
import duckdb
import pandas as pd
# from pipe import ELTPipeline
from query import Querydb


ui.page_opts(title = "Countries' Olympic Medals vs their Population and GDP",
             fillable=True,
             page_fn = partial(page_navbar, id = "page"))

with ui.nav_control():
    ui.input_dark_mode()

with ui.nav_panel("Medals"):

    with ui.card():

        ui.markdown("Olympic Total Medal Count By Country.")

        ui.input_numeric("n", "Number of items in bar plot", 5, min = 1, max = 90)

    with ui.layout_columns():
        @render_plotly
        def total_medals_plot():
            df = getdata()
            top_n = df.groupby('country_code')['total'].sum().nlargest(input.n()).reset_index()
            return px.bar(top_n, x = 'country_code', y = 'total')

    with ui.card():
    
        ui.markdown("Gold, Silver and Bronze medals.")

        ui.input_numeric("gn", "Number of items in bar plot", 5, min = 1, max = 90)

        ui.input_selectize("medalselect", "Select medal category.",
                        {"gold":"Gold Medal", "silver":"Silver Medal", "bronze":"Bronze Medal"})

    with ui.layout_columns():
        @render_plotly
        def gold_medals_plot():
            df = getdata()
            gold_n = df.groupby('country_code')[input.medalselect()].sum().nlargest(input.gn()).reset_index()
            return px.bar(gold_n, x = 'country_code' , y = input.medalselect())

with ui.nav_panel("GDP"):
    with ui.card():

        ui.markdown("GDP by Country.")

        ui.input_numeric("gdpn", "Number of items in bar plot", 5, min = 1, max = 90)

    with ui.layout_columns():
        @render_plotly
        def gdp_plot():
            df = getdata()
            gdp_n = df.groupby('country_code')['gdp'].sum().nlargest(input.gdpn()).reset_index()
            return px.bar(gdp_n, x = 'country_code', y = 'gdp')

with ui.nav_panel("Population"):
    with ui.card():

        ui.markdown("Population by Country.")

        ui.input_numeric("ppn", "Number of items in bar plot", 5, min = 1, max = 90)
    
    with ui.layout_columns():
        @render_plotly
        def population_plot():
            df = getdata()
            population_n = df.groupby('country_code')['population'].sum().nlargest(input.ppn()).reset_index()
            return px.bar(population_n, x = 'country_code', y = 'population')

with ui.nav_panel("Raw Data"):
    with ui.card():

        ui.markdown("Raw Data")

        @render.data_frame
        def showtable():
            return getdata()

@reactive.calc
def getdata():
    querydata = Querydb()
 
    #Fetch all data
    df = querydata.query_postgre_duck() 

    return df