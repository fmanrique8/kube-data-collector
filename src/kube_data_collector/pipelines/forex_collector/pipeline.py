"""
This is a boilerplate pipeline 'forex_collector'
generated using Kedro 0.18.12
"""

from kedro.pipeline import Pipeline, node
from .nodes import forex_data_collector_node


def create_pipeline() -> Pipeline:
    """
    Creates the 'forex_collector' pipeline.

    Returns:
        Pipeline: Kedro pipeline object containing the forex_data_collector_node.
    """
    # Define nodes for each config_name
    forex_node_10_min = node(
        func=forex_data_collector_node,
        inputs=[
            "params:config_name",
            "params:access_token",
            "params:accountID",
            "params:base_url",
            "params:endpoint",
            "params:forex_collector_config",
        ],
        outputs="10_min_dataframe",
        name="forex_data_collector_node_10_min",
    )

    forex_node_15_min = node(
        func=forex_data_collector_node,
        inputs=[
            "params:config_name",
            "params:access_token",
            "params:accountID",
            "params:base_url",
            "params:endpoint",
            "params:forex_collector_config",
        ],
        outputs="15_min_dataframe",
        name="forex_data_collector_node_15_min",
    )

    forex_node_30_min = node(
        func=forex_data_collector_node,
        inputs=[
            "params:config_name",
            "params:access_token",
            "params:accountID",
            "params:base_url",
            "params:endpoint",
            "params:forex_collector_config",
        ],
        outputs="30_min_dataframe",
        name="forex_data_collector_node_30_min",
    )

    # Return the pipeline containing these nodes
    return Pipeline([forex_node_10_min, forex_node_15_min, forex_node_30_min])
