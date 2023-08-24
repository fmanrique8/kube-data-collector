"""
This is a boilerplate pipeline 'forex_model_input'
generated using Kedro 0.18.12
"""

from kedro.pipeline import Pipeline, node
from .nodes import forex_model_input_node


def create_pipeline() -> Pipeline:
    """Creates the 'forex_model_input' pipeline.

    Returns:
        Pipeline: Kedro pipeline object containing the data processing nodes.
    """

    model_input_10_min_node = node(
        func=forex_model_input_node,
        inputs=[
            "10_min_primary",
        ],
        outputs=[
            "10_min_model_input",
            "10_min_t3_model_input",
            "10_min_l3_model_input",
        ],
        name="forex_model_input_node_10_min",
    )

    model_input_15_min_node = node(
        func=forex_model_input_node,
        inputs=[
            "15_min_primary",
        ],
        outputs=[
            "15_min_model_input",
            "15_min_t3_model_input",
            "15_min_l3_model_input",
        ],
        name="forex_model_input_node_15_min",
    )

    model_input_30_min_node = node(
        func=forex_model_input_node,
        inputs=[
            "30_min_primary",
        ],
        outputs=[
            "30_min_model_input",
            "30_min_t3_model_input",
            "30_min_l3_model_input",
        ],
        name="forex_model_input_node_30_min",
    )

    # Return the pipeline containing these nodes
    return Pipeline(
        [model_input_10_min_node, model_input_15_min_node, model_input_30_min_node]
    )
