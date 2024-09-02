#!/usr/bin/env python
import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output, State
import geopandas as gpd
import pandas as pd
import plotly.graph_objects as go

from map_config import variables, variable_labels, dimension_labels, order


def main():
    # Reading in geometry data
    eaz = gpd.read_file("atx_eaz_multi_year.geojson")
    geojson = eaz.__geo_interface__

    # Household income was set as negative
    eaz["median_hh_inc"] = eaz["median_hh_inc"] * -1

    # Identifying first and last year
    min_year = eaz["acs_year"].min()
    max_year = eaz["acs_year"].max()

    # Flipping the dataframe so each row is a year's variable
    id_variables = ["GEOID", "acs_year", "geometry", "NAME", "eaz_type"]
    df_long = eaz.melt(
        id_vars=id_variables, var_name="variable", value_name="value"
    )
    df_long = df_long[df_long["variable"].isin(variables)]
    df_long["value"] = df_long["value"].astype(float)

    # Getting base year data
    base_year = df_long[df_long["acs_year"] == min_year]
    base_year = base_year[["GEOID", "variable", "value"]]
    base_year.rename(columns={"value": "base_year_value"}, inplace=True)

    # join base year data back to original data
    df_difference = df_long.merge(base_year, on=["GEOID", "variable"], how="left")
    df_difference["value"] = df_difference["value"] - df_difference["base_year_value"]
    df_difference.drop(["base_year_value"], axis=1, inplace=True)
    df_difference["dimension"] = "relative"
    df_long["dimension"] = "absolute"

    # combining both absolute and relative measures
    df_long = pd.concat([df_difference, df_long])

    # Data for the bar plot
    eaz_type = eaz[["GEOID", "eaz_type", "acs_year"]]
    return df_long, eaz_type, geojson


long_data, eaz_type, geojson = main()

# ### Creating plotly visualization

order_mapping = {name: i for i, name in enumerate(order)}

# Create the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define the layout of the Dash app
app.layout = dbc.Container(
    [
        dbc.Row(
            dbc.Col(
                html.H1(
                    "Equity Analysis Zones Yearly Comparison Tool",
                    className="mb-3 text-center",
                ),
                width=12,
            ),
            className="justify-content-center",
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Label("Select Variable"),
                        dcc.Dropdown(
                            id="variable-dropdown",
                            options=[
                                {"label": variable_labels[var], "value": var}
                                for var in long_data["variable"].unique()
                            ],
                            value="indexed_vulnerability",
                            className="mb-3",
                            clearable=False,
                        ),
                    ],
                    width=4,
                ),
                dbc.Col(
                    [
                        dbc.Label("Select Dimension"),
                        dcc.Dropdown(
                            id="dimension-dropdown",
                            options=[
                                {"label": dimension_labels[dim], "value": dim}
                                for dim in long_data["dimension"].unique()
                            ],
                            value="absolute",
                            className="mb-3",
                            clearable=False,
                        ),
                    ],
                    width=4,
                ),
                dbc.Col(
                    [
                        dbc.Label("Select Year"),
                        dcc.Dropdown(
                            id="year-dropdown",
                            options=[
                                {"label": str(year), "value": year}
                                for year in long_data["acs_year"].unique()
                            ],
                            value=2019,
                            className="mb-3",
                            clearable=False,
                        ),
                    ],
                    width=4,
                ),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(dcc.Graph(id="choropleth-map"), width=8),
                dbc.Col(dcc.Graph(id="bar-plot"), width=4),
            ]
        ),
    ],
    fluid=True,
)


# Define the callback to update the plot based on dropdown selections
@app.callback(
    [Output("choropleth-map", "figure"), Output("bar-plot", "figure")],
    [
        Input("variable-dropdown", "value"),
        Input("dimension-dropdown", "value"),
        Input("year-dropdown", "value"),
    ],
)
def update_plots(selected_variable, selected_dimension, selected_year):
    filtered_data = long_data[
        (long_data["variable"] == selected_variable)
        & (long_data["dimension"] == selected_dimension)
        & (long_data["acs_year"] == selected_year)
        ]

    # Configuring the hover template
    customdata = filtered_data[["NAME", "acs_year"]].copy()

    # Chloropleth traces
    hovertemplate = (
            "<b>%{customdata[0]}</b><br>"
            + "<b>Year:</b> %{customdata[1]}<br>"
            + "<b>"
            + variable_labels[selected_variable]
            + " "
            + dimension_labels[selected_dimension]
            + ":</b> %{z:.2f}<br>"
    )

    if selected_dimension == "relative":
        scale = "puor"
        midpoint = 0
    else:
        scale = "Viridis"
        midpoint = None

    # Choropleth map
    choropleth_fig = go.Figure()
    choropleth_fig.add_trace(
        go.Choroplethmapbox(
            locations=filtered_data["GEOID"],
            geojson=geojson,
            featureidkey="properties.GEOID",
            z=filtered_data["value"],
            name="",
            colorscale=scale,
            zmid=midpoint,
            marker_opacity=0.8,
            marker_line_width=0.25,
            hovertemplate=hovertemplate,
            customdata=customdata,
            colorbar=dict(
                x=0.1,
                y=-0.015,
                thickness=10,
                outlinecolor="rgba(0,0,0,0)",  # Transparent outline
                bgcolor="rgba(255,255,255,1)",  # White background
                len=0.2,
                orientation="h",
            ),
            hoverlabel=dict(
                bgcolor="white"  # Change background color of the hover label
            ),
        )
    )

    choropleth_fig.update_layout(
        title_text=f"{variable_labels[selected_variable]}<br><sup>{dimension_labels[selected_dimension]}-{selected_year}</sup>",
        title_font=dict(size=20),
        title_x=0.5,
        mapbox_style="carto-positron",
        height=700,
        mapbox_zoom=8,
        mapbox_center={"lat": 30.2672, "lon": -97.7431},  # Austin coordinates
    )

    # Bar plot
    filtered_data_bar = eaz_type[(eaz_type["acs_year"] == selected_year)]
    bar_data = filtered_data_bar[["eaz_type"]].value_counts().reset_index()
    bar_data.columns = ["eaz_type", "count"]
    bar_data["order"] = bar_data["eaz_type"].map(order_mapping)
    bar_data = bar_data.sort_values("order")  # Sort by the specified order
    bar_fig = go.Figure()
    bar_fig.add_trace(
        go.Bar(
            x=bar_data["eaz_type"],
            y=bar_data["count"],
            hovertemplate=(
                    "<b>Number of census tracts:</b> %{y}<br>" + "<extra></extra>"
            ),
        )
    )
    bar_fig.update_layout(
        title=f"Census tracts by vulnerability index<br><sup>{selected_year}</sup>",
        title_x=0.5,
        title_font=dict(size=20),
        height=700,
        plot_bgcolor="rgba(0,0,0,0)",
        hoverlabel=dict(bgcolor="white"),  # Change background color of the hover label
    )

    bar_fig.update_xaxes(
        tickmode="array",
        tickvals=[0, 1, 2, 3, 4],
        ticktext=[
            "Least<br>Vulnerable",
            "Medium-Low<br>Vulnerable",
            "Medium<br>Vulnerable",
            "Medium-High<br>Vulnerable",
            "Most<br>Vulnerable",
        ],
        tickfont=dict(size=11),
        tickangle=0,
    )

    bar_fig.update_yaxes(gridcolor="lightgray")
    return choropleth_fig, bar_fig


# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
