"""
This is a boilerplate pipeline 'forex_feature'
generated using Kedro 0.18.12
"""

from kedro.pipeline import Pipeline, node
from .nodes import forex_feature_node


def create_pipeline() -> Pipeline:
    """Creates the 'forex_primary' pipeline.

    Returns:
        Pipeline: Kedro pipeline object containing the data processing nodes.
    """

    feature_10_min_node = node(
        func=forex_feature_node,
        inputs=[
            "10_min_primary",
        ],
        outputs="10_min_feature",
        name="forex_feature_node_10_min",
    )

    feature_15_min_node = node(
        func=forex_feature_node,
        inputs=[
            "15_min_primary",
        ],
        outputs="15_min_feature",
        name="forex_feature_node_15_min",
    )

    feature_30_min_node = node(
        func=forex_feature_node,
        inputs=[
            "30_min_primary",
        ],
        outputs="30_min_feature",
        name="forex_feature_node_30_min",
    )

    # Return the pipeline containing these nodes
    return Pipeline([feature_10_min_node, feature_15_min_node, feature_30_min_node])
