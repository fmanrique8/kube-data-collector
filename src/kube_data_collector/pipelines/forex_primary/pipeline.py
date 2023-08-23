"""
This is a boilerplate pipeline 'forex_primary'
generated using Kedro 0.18.12
"""

from kedro.pipeline import Pipeline, node
from .nodes import forex_primary_node


def create_pipeline() -> Pipeline:
    """Creates the 'forex_primary' pipeline.

    Returns:
        Pipeline: Kedro pipeline object containing the data processing nodes.
    """

    primary_10_min_node = node(
        func=forex_primary_node,
        inputs=[
            "10_min_intermediate",
            "params:primary_data_config.configurations.roc_periods.10_min",
            "params:primary_data_config.configurations.rsi_periods.10_min",
            "params:primary_data_config.configurations.stochastic_oscillator_periods.10_min",
        ],
        outputs="10_min_primary",
        name="forex_primary_node_10_min",
    )

    primary_15_min_node = node(
        func=forex_primary_node,
        inputs=[
            "15_min_intermediate",
            "params:primary_data_config.configurations.roc_periods.15_min",
            "params:primary_data_config.configurations.rsi_periods.15_min",
            "params:primary_data_config.configurations.stochastic_oscillator_periods.15_min",
        ],
        outputs="15_min_primary",
        name="forex_primary_node_15_min",
    )

    primary_30_min_node = node(
        func=forex_primary_node,
        inputs=[
            "30_min_intermediate",
            "params:primary_data_config.configurations.roc_periods.30_min",
            "params:primary_data_config.configurations.rsi_periods.30_min",
            "params:primary_data_config.configurations.stochastic_oscillator_periods.30_min",
        ],
        outputs="30_min_primary",
        name="forex_primary_node_30_min",
    )

    # Return the pipeline containing these nodes
    return Pipeline([primary_10_min_node, primary_15_min_node, primary_30_min_node])
