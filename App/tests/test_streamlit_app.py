from io import BytesIO

from PIL import Image

from App import streamlit_app
from App.services.dashboard_metrics import compute_dashboard_metrics
from App.services.pipeline_runner import run_analysis
from pipeline.schema import (
    AnalyseResultat,
    BoundingBox,
    DetectedObject,
    PipelineOutput,
    RisqueEvaluation,
    SceneDetections,
)


def _build_sample_output() -> PipelineOutput:
    detections = SceneDetections(
        detected_objects=[
            DetectedObject(
                label="car",
                confidence=0.9,
                bounding_box=BoundingBox(x=10, y=20, width=80, height=60),
                relative_position="center-near",
            ),
            DetectedObject(
                label="person",
                confidence=0.75,
                bounding_box=BoundingBox(x=120, y=30, width=30, height=70),
                relative_position="left-mid",
            ),
            DetectedObject(
                label="truck",
                confidence=0.85,
                bounding_box=BoundingBox(x=180, y=40, width=100, height=80),
                relative_position="right-near",
            ),
        ]
    )
    analysis = AnalyseResultat(
        resume="Scene chargee avec plusieurs usagers.",
        recommandations=["Ralentir", "Rester centre dans la voie"],
        risque_eval=RisqueEvaluation(risque_level="Moyen"),
    )
    return PipelineOutput(scene_detections=detections, analyse_resultat=analysis)


class FakeRunner:
    def __init__(self, expected_result: PipelineOutput):
        self.expected_result = expected_result
        self.received_stream = None

    def run_pipeline(self, uploaded_file):
        self.received_stream = uploaded_file
        return self.expected_result


def test_run_analysis_uses_injected_runner_and_rewinds_file():
    expected_result = _build_sample_output()
    runner = FakeRunner(expected_result)
    uploaded_file = BytesIO(b"fake-image-bytes")
    uploaded_file.seek(4)

    result = run_analysis(uploaded_file, runner=runner)

    assert result == expected_result
    assert runner.received_stream is uploaded_file
    assert uploaded_file.tell() == 0


def test_compute_dashboard_metrics_aggregates_scene_data():
    output = _build_sample_output()

    metrics = compute_dashboard_metrics(output.scene_detections)

    assert metrics.total_objects == 3
    assert metrics.vehicle_count == 2
    assert metrics.people_count == 1
    assert metrics.near_objects == 2
    assert metrics.top_label in {"car", "person", "truck"}
    assert round(metrics.average_confidence, 2) == 0.83
    assert metrics.label_counts["car"] == 1


def test_main_shows_info_when_no_file_uploaded(monkeypatch):
    calls = {"info": None, "run_analysis_called": False, "render_results_called": False}

    monkeypatch.setattr(streamlit_app, "configure_page", lambda: None)
    monkeypatch.setattr(streamlit_app, "apply_styles", lambda: None)
    monkeypatch.setattr(streamlit_app, "render_header", lambda: None)
    monkeypatch.setattr(streamlit_app, "render_uploader", lambda: (None, None))
    monkeypatch.setattr(
        streamlit_app,
        "run_analysis",
        lambda uploaded_file: calls.__setitem__("run_analysis_called", True),
    )
    monkeypatch.setattr(
        streamlit_app,
        "render_results",
        lambda image, result: calls.__setitem__("render_results_called", True),
    )
    monkeypatch.setattr(
        streamlit_app.st,
        "info",
        lambda message: calls.__setitem__("info", message),
    )

    streamlit_app.main()

    assert calls["info"] == "Veuillez uploader une image JPG"
    assert calls["run_analysis_called"] is False
    assert calls["render_results_called"] is False


def test_main_runs_analysis_and_renders_results(monkeypatch):
    calls = {"render_results_args": None}
    output = _build_sample_output()
    image = Image.new("RGB", (100, 80), color="white")
    uploaded_file = BytesIO(b"raw-data")

    monkeypatch.setattr(streamlit_app, "configure_page", lambda: None)
    monkeypatch.setattr(streamlit_app, "apply_styles", lambda: None)
    monkeypatch.setattr(streamlit_app, "render_header", lambda: None)
    monkeypatch.setattr(streamlit_app, "render_uploader", lambda: (uploaded_file, image))
    monkeypatch.setattr(streamlit_app, "run_analysis", lambda given_file: output)
    monkeypatch.setattr(
        streamlit_app,
        "render_results",
        lambda given_image, given_result: calls.__setitem__(
            "render_results_args",
            (given_image, given_result),
        ),
    )

    streamlit_app.main()

    assert calls["render_results_args"] == (image, output)
