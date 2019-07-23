import shutil

from tf_explain.callbacks.activations_visualization import (
    ActivationsVisualizationCallback,
)


def test_should_call_activations_visualization_callback(
    random_data, convolutional_model, output_dir, mocker
):
    mock_explainer = mocker.MagicMock()
    mock_explainer.explain = mocker.MagicMock(return_value=mocker.sentinel.grid)
    mock_explainer.save = mocker.MagicMock()
    mocker.patch(
        "tf_explain.callbacks.activations_visualization.ExtractActivations",
        return_value=mock_explainer,
    )

    images, labels = random_data

    callbacks = [
        ActivationsVisualizationCallback(
            validation_data=random_data,
            layers_name=["activation_1"],
            output_dir=output_dir,
        )
    ]

    convolutional_model.fit(images, labels, batch_size=2, epochs=1, callbacks=callbacks)

    mock_explainer.explain.assert_called_once_with(
        random_data, convolutional_model, ["activation_1"]
    )
    mock_explainer.save.assert_called_once_with(
        mocker.sentinel.grid, output_dir, "0.png"
    )

    shutil.rmtree(output_dir)
