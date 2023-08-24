"""
This is a boilerplate pipeline 'forex_processor'
generated using Kedro 0.18.12
"""

from kedro.pipeline import Pipeline, node
from .nodes import data_processor_node


def create_pipeline() -> Pipeline:
    """
    Creates the 'forex_processor' pipeline.

    Returns:
        Pipeline: Kedro pipeline object containing the data processing nodes.
    """
    # Define nodes for processing each dataframe

    process_10_min_node = node(
        func=data_processor_node,
        inputs="10_min_dataframe",
        outputs="10_min_intermediate",
        name="data_processor_node_10_min",
    )

    process_15_min_node = node(
        func=data_processor_node,
        inputs="15_min_dataframe",
        outputs="15_min_intermediate",
        name="data_processor_node_15_min",
    )

    process_30_min_node = node(
        func=data_processor_node,
        inputs="30_min_dataframe",
        outputs="30_min_intermediate",
        name="data_processor_node_30_min",
    )

    # Return the pipeline containing these nodes
    return Pipeline([process_10_min_node, process_15_min_node, process_30_min_node])
