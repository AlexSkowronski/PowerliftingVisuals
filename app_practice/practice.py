from dash import Output, Input, dcc, html
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd

def call_data(address:str):
    df = pd.read_csv(address)
    relevant_columns = ["Name", "Sex", "Event", "AgeClass"]

df = pd.read_csv("../data.csv")
