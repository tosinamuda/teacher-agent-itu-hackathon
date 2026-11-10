"""Dashboard DTO assembly for the experiments domain.

Every service takes only the role-facing readers it needs, so the transport
layer selects an endpoint, parses request DTOs and delegates. Nothing here
writes — ``tests/test_read_write_seam.py`` pins that.
"""

from app.domains.experiments.application.experiment_views.execution import (
    ExperimentExecutionViewQuery,
    ExperimentExecutionViewReader,
    build_execution_detail_view,
    execution_payload,
    execution_response,
    render_evaluation_packet_response,
)
from app.domains.experiments.application.experiment_views.experiment import (
    ExperimentListQuery,
    ExperimentView,
    ExperimentViewQuery,
    build_experiment_detail_view,
    build_experiment_view,
    experiment_view,
    list_experiment_views,
)
from app.domains.experiments.application.experiment_views.experiment_response import (
    matches_experiment_query,
)
from app.domains.experiments.application.experiment_views.options import (
    list_workspace_lesson_approved_versions,
    list_workspace_lesson_options,
    list_workspace_options,
)
from app.domains.experiments.application.experiment_views.synthetic_students import (
    SyntheticStudentContextQuery,
    resolve_synthetic_students_context,
)

__all__ = [
    "ExperimentView",
    "ExperimentExecutionViewReader",
    "ExperimentExecutionViewQuery",
    "ExperimentListQuery",
    "ExperimentViewQuery",
    "SyntheticStudentContextQuery",
    "build_execution_detail_view",
    "build_experiment_detail_view",
    "build_experiment_view",
    "execution_payload",
    "execution_response",
    "experiment_view",
    "list_experiment_views",
    "list_workspace_lesson_approved_versions",
    "list_workspace_lesson_options",
    "list_workspace_options",
    "matches_experiment_query",
    "render_evaluation_packet_response",
    "resolve_synthetic_students_context",
]
