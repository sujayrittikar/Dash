import pymongo.errors as mongo_errors
import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.express as px

from dash_project.mongo_conn import get_mongo_conn


MONGO_CLIENT = get_mongo_conn()
CITIES_DB = MONGO_CLIENT.cities
CITIES_REDDIT_COLLECTION = CITIES_DB.cities_reddit

APP = Dash(__name__)
METRICS = ["Mean", "Median", "Max", "Min", "Sum", "Test"]


def read_df_from_mongo() -> pd.DataFrame:
    """
        Returns a Dataframe with all data in Mongodb
    """
    reddit_posts = CITIES_REDDIT_COLLECTION.find()
    reddit_posts_df = pd.DataFrame(reddit_posts)
    return reddit_posts_df


def get_aggregated_karmas(
        dataframe: pd.DataFrame,
        metric: str
     ) -> pd.DataFrame:
    """
        Returns aggregated Karma Subreddit wise based on Dataframe
    """
    agg_generic_df = dataframe.groupby(by=["subreddit"], dropna=True)

    if metric == "Mean":
        agg_mt_df = agg_generic_df.mean()
        agg_mt_df.rename(columns={"karma": "Mean Karma"}, inplace=True)
    elif metric == "Max":
        agg_mt_df = agg_generic_df.max()
        agg_mt_df.rename(columns={"karma": "Max Karma"}, inplace=True)
    elif metric == "Min":
        agg_mt_df = agg_generic_df.min()
        agg_mt_df.rename(columns={"karma": "Min Karma"}, inplace=True)
    elif metric == "Median":
        agg_mt_df = agg_generic_df.median()
        agg_mt_df.rename(columns={"karma": "Median Karma"}, inplace=True)
    elif metric == "Sum":
        agg_mt_df = agg_generic_df.sum()
        agg_mt_df.rename(columns={"karma": "Sum Karma"}, inplace=True)
    else:
        agg_mt_df = pd.DataFrame()

    return agg_mt_df


def get_aggregated_karmas_from_db(metric: str) -> pd.DataFrame:
    """
        Returns aggregated Karma Subreddit wise based on MongoDB
    """
    aggregation_op = ""
    if metric == "Mean":
        aggregation_op = "$avg"
    elif metric == "Max":
        aggregation_op = "$max"
    elif metric == "Min":
        aggregation_op = "$min"
    elif metric == "Sum":
        aggregation_op = "$sum"

    aggregation_results = CITIES_REDDIT_COLLECTION.aggregate([
        {
            "$group":
            {
                "_id": "$subreddit",
                metric+" Karma":
                {aggregation_op: "$karma"}
            }
        }
    ])

    agg_df = pd.DataFrame(aggregation_results)
    agg_df.rename(columns={"_id": "subreddit"}, inplace=True)

    return agg_df


def render_dash_app() -> None:
    """
        The Core of rendering the Graphs
    """
    APP.layout = html.Div([
        html.H1(children="Subreddit Karma Analysis", style={
            "textAlign": "center"
        }),
        html.P("Choose a Metric to check the City wise Karmas with"),
        dcc.Dropdown(METRICS, "Mean", id="metric_dropdown"),
        dcc.Graph(id="dd-output-container")
    ])

    @APP.callback(
        Output('dd-output-container', 'figure'),
        Input('metric_dropdown', 'value')
    )


    def update_output(value) -> px.bar:
        """
            The callback function to render the figure
        """
        try:
            if value == "Median":
                data = read_df_from_mongo()
                agg_df = get_aggregated_karmas(data, value)
                x_axis = agg_df.index
            else:
                agg_df = get_aggregated_karmas_from_db(value)
                x_axis = "subreddit"
        except mongo_errors.OperationFailure:
            return px.bar()

        try:
            figure = px.bar(
                agg_df,
                x=x_axis,
                y=value + ' Karma',
                title="City Wise Subreddit Karmas"
            )
            figure.update_layout(
                barmode="stack",
                xaxis={"categoryorder": "total descending"}
            )
            return figure
        except ValueError:
            return px.bar()

    APP.run(debug=True)


def main() -> int:
    render_dash_app()
    return 0


if __name__ == "__main__":
    main()
