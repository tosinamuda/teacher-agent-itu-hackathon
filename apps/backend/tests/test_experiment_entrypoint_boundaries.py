"""Ratchet the experiments transport-to-application boundary.

Every baseline here is an exact set, not a ceiling. Adding a violation fails; removing one
fails too, until the baseline is shrunk in the same change — so the recorded debt can only
go down, and the census cannot silently drift from the code.

The rule these guards enforce is ``docs/application-boundaries.md``; the human-readable
classification is ``docs/experiments-entrypoint-census.md``.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from tests.application_operation_shape import operation_shape
from tests.entrypoint_census import experiments_entrypoints
from tests.mechanism_types import MECHANISM_LAYER, import_origins, mechanism_types_in_source

pytestmark = pytest.mark.architecture

CENSUS_DOCUMENT = Path("docs/experiments-entrypoint-census.md")
APPLICATION = Path("src/app/domains/experiments/application")
SQLALCHEMY = "from sqlalchemy"

# The rule names four injected roles as the point where a route is assembling the use case.
MAX_INJECTED_COLLABORATORS = 3

# Entrypoint -> the application operation it invokes.
CENSUS: dict[str, str] = {
    "create_investigation": "create_investigation_command",
    "list_investigations": "InvestigationApplicationService.list_investigations",
    "get_investigation": "InvestigationApplicationService.get_investigation",
    "end_investigation": "end_investigation_command",
    "list_experiment_workspaces": "list_workspace_options",
    "list_workspace_lessons": "list_workspace_lesson_options",
    "list_workspace_lesson_versions": "list_workspace_lesson_approved_versions",
    "create_experiment": "ExperimentApplicationService.create_experiment",
    "author_experiment_plan": "ExperimentApplicationService.check_plan_authoring",
    "draft_experiment_plan": "ExperimentApplicationService.draft_experiment_plan",
    "author_experiment_plan_manual": "ExperimentApplicationService.author_experiment_plan_manual",
    "reuse_experiment_plan": "ExperimentPlanReuse",
    "freeze_experiment_plan": "ExperimentApplicationService.freeze_experiment_plan",
    "create_experiment_review_note": "ExperimentApplicationService.create_review_note",
    "author_experiment_classwork_manual": (
        "ExperimentApplicationService.author_experiment_classwork_manual"
    ),
    "list_experiments": "ExperimentListQuery.list_experiments",
    "update_focal_learners": "update_focal_learners_command",
    "end_experiment": "end_experiment_command",
    "set_experiment_sandbox": "set_sandbox_command",
    "get_research_defaults": "none",
    "get_experiment_story": "ExperimentStoryApplicationService.build_experiment_story",
    "get_experiment": "ExperimentViewQuery.build_detail",
    "get_experiment_summary": "ExperimentViewQuery.build_view",
    "get_experiment_workflow": "ExperimentWorkflowQuery.compute",
    "get_experiment_provenance": "StudyRecordQuery.provenance",
    "get_rater_schedule": "StudyRecordQuery.schedule",
    "get_study_results": "StudyRecordQuery.results",
    "get_study_wide_results": "StudyRecordQuery.study_results",
    "get_transcripts": "StudyRecordQuery.transcripts",
    "get_study_design": "StudyRecordQuery.design",
    "create_experiment_execution": "LaunchExecution",
    "retry_experiment_condition": "retry_condition",
    "trigger_synthetic_students": "none",
    "trigger_synthetic_rate": "none",
    "trigger_synthetic_teacher": "none",
    "trigger_synthetic_loop": "none",
    "synthetic_progress_ws": "none",
    "get_execution": "ExperimentExecutionViewQuery.build_detail",
    "export_execution_packets": "PacketExportApplicationService.export_packets",
    "retry_failed_condition": "retry_failed_condition",
    "conduct_conditioned_execution": "conduct_conditioned_execution",
}

# Transports that still receive the request session and decide for themselves when to commit.
RAW_SESSION_ENTRYPOINTS = {
    "author_experiment_classwork_manual",
    "author_experiment_plan",
    "author_experiment_plan_manual",
    "create_experiment",
    "create_experiment_review_note",
    "freeze_experiment_plan",
    "get_experiment_story",
}

# Transports that name a concrete repository, ORM row, or SQLAlchemy store in their signature.
CONCRETE_PERSISTENCE_ENTRYPOINTS: set[str] = set()

# Transports that receive enough roles to sequence the use case themselves.
WORKFLOW_ASSEMBLY_ENTRYPOINTS = {
    "author_experiment_plan_manual",
    "create_experiment_review_note",
    "freeze_experiment_plan",
}

# Application callables already shaped as one input to one output.
RECOGNIZED_OPERATIONS = {"LaunchExecution"}

# Scripts and harnesses reaching into experiments persistence for want of an operation to call.
PERSISTENCE_READING_HARNESSES = {
    Path("experiments/p1_evidence_prompt/runner.py"),
    Path("experiments/p1_prompt_eval/dataset.py"),
    Path("scripts/seed_jss1_curriculum.py"),
    #: The study import writes the concluded study's rows, as the seed writes the curriculum.
    Path("experiments/study_import/importer.py"),
    Path("experiments/study_import/runs.py"),
    Path("experiments/study_import/transcript_rows.py"),
    Path("experiments/study_import/withdraw.py"),
}

LAUNCH_OPERATIONS = {
    "LaunchExecution": APPLICATION / "execution_launch.py",
    "retry_condition": APPLICATION / "execution_launch.py",
    "create_execution": APPLICATION / "create_execution.py",
    "retry_failed_condition": APPLICATION / "condition_retry.py",
    "conduct_conditioned_execution": APPLICATION / "conditioned_execution.py",
}

CANONICAL_OPERATION = """
from dataclasses import dataclass

from app.domains.experiments.application.launch_roles import ExecutionLaunchStore
from app.domains.experiments.domain import ExecutionStatus


@dataclass(frozen=True)
class LaunchExecutionInput:
    experiment_id: str


@dataclass(frozen=True)
class LaunchExecutionOutput:
    execution_id: str
    status: ExecutionStatus


class LaunchExecution:
    def __init__(self, store: ExecutionLaunchStore) -> None:
        self._store = store

    async def __call__(self, request: LaunchExecutionInput) -> LaunchExecutionOutput: ...
"""

PER_CALL_COLLABORATORS = """
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.experiments.infrastructure.models import ExperimentExecution


class LaunchExecution:
    async def __call__(self, db: AsyncSession, experiment_id: str) -> ExperimentExecution: ...
"""


def _document_handlers() -> set[str]:
    rows = CENSUS_DOCUMENT.read_text().splitlines()
    cells = (re.findall(r"`([^`]+)`", row) for row in rows if row.startswith("|"))
    return {found[1] for found in cells if len(found) >= 2}


def test_every_experiments_entrypoint_is_classified() -> None:
    assert {entrypoint.name for entrypoint in experiments_entrypoints()} == set(CENSUS)


def test_census_document_matches_the_enforced_census() -> None:
    assert _document_handlers() == set(CENSUS)


def _entrypoints_naming(origin_marker: str) -> set[str]:
    """Entrypoints whose signature names a type declared in a matching module."""
    offenders: set[str] = set()
    for entrypoint in experiments_entrypoints():
        origins = import_origins(Path(entrypoint.location.rsplit(":", 1)[0]))
        found = [
            named
            for annotation in entrypoint.annotations
            for named in mechanism_types_in_source(annotation, origins)
            if origin_marker in named
        ]
        if found:
            offenders.add(entrypoint.name)
    return offenders


def test_transports_do_not_receive_the_request_session() -> None:
    assert _entrypoints_naming(SQLALCHEMY) == RAW_SESSION_ENTRYPOINTS


def test_transports_do_not_name_concrete_persistence() -> None:
    assert _entrypoints_naming(MECHANISM_LAYER) == CONCRETE_PERSISTENCE_ENTRYPOINTS


def test_transports_do_not_assemble_multi_role_workflows() -> None:
    offenders = {
        entrypoint.name
        for entrypoint in experiments_entrypoints()
        if len(entrypoint.collaborators) > MAX_INJECTED_COLLABORATORS
    }
    assert offenders == WORKFLOW_ASSEMBLY_ENTRYPOINTS


def test_scripts_and_harnesses_do_not_read_experiments_persistence() -> None:
    offenders = {
        path
        for root in (Path("scripts"), Path("experiments"))
        for path in root.rglob("*.py")
        if "app.domains.experiments.infrastructure" in path.read_text()
    }
    assert offenders == PERSISTENCE_READING_HARNESSES


def test_recognized_application_operations_match_the_baseline() -> None:
    recognized = {
        symbol
        for symbol, path in LAUNCH_OPERATIONS.items()
        if operation_shape(path, symbol).conforms
    }
    assert recognized == RECOGNIZED_OPERATIONS


def test_launch_is_the_first_transport_neutral_operation() -> None:
    """One input, one output, store bound at construction — no mechanism type in either."""
    shape = operation_shape(APPLICATION / "execution_launch.py", "LaunchExecution")
    assert shape.reasons == ()


def test_the_ratchet_recognizes_the_canonical_operation(tmp_path: Path) -> None:
    path = tmp_path / "launch.py"
    path.write_text(CANONICAL_OPERATION)
    assert operation_shape(path, "LaunchExecution").conforms


def test_the_ratchet_rejects_per_call_collaborators_and_mechanism_contracts(
    tmp_path: Path,
) -> None:
    path = tmp_path / "launch.py"
    path.write_text(PER_CALL_COLLABORATORS)
    shape = operation_shape(path, "LaunchExecution")
    assert shape.reasons == (
        "takes 2 per-call parameters; an operation takes one input",
        "parameter 'db' carries AsyncSession from sqlalchemy.ext.asyncio",
        "output carries ExperimentExecution from app.domains.experiments.infrastructure.models",
    )


def test_the_ratchet_does_not_mistake_a_protocol_for_an_operation() -> None:
    shape = operation_shape(APPLICATION / "launch_ports.py", "ExecutionLaunchStore")
    assert shape.reasons == ("is a Protocol; it describes a collaborator, not an operation",)
