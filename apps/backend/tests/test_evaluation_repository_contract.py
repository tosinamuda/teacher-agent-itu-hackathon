"""Static contract for evaluation's constructor-bound persistence adapter."""

from __future__ import annotations

import inspect

from app.domains.evaluation.application.assignment_queries import (
    AssignmentViewReader,
    MyQueueReader,
    RaterListReader,
)
from app.domains.evaluation.application.audit_queries import (
    AuditDetailReader,
    AuditExportReader,
    AuditQueueReader,
)
from app.domains.evaluation.application.dataset_queries import DatasetData
from app.domains.evaluation.application.experiment_statistics import ExperimentStatisticsData
from app.domains.evaluation.application.investigation_rollup import InvestigationRollupData
from app.domains.evaluation.application.packet_ports import (
    H1PacketDetailData,
    H2PacketDetailData,
    PacketQueueData,
)
from app.domains.evaluation.application.ratings_summary import RatingsSummaryData
from app.domains.evaluation.infrastructure.repository import EvaluationRepository


def test_repository_requires_one_session_at_construction() -> None:
    signature = inspect.signature(EvaluationRepository)

    assert list(signature.parameters) == ["session"]


def test_public_repository_methods_do_not_accept_sessions() -> None:
    for name, method in inspect.getmembers(EvaluationRepository, inspect.iscoroutinefunction):
        if name.startswith("_"):
            continue
        parameters = inspect.signature(method).parameters
        assert "db" not in parameters, name
        assert "session" not in parameters, name


def test_read_ports_have_no_transaction_capability() -> None:
    read_ports = (
        PacketQueueData,
        H1PacketDetailData,
        H2PacketDetailData,
        AuditQueueReader,
        AuditDetailReader,
        AuditExportReader,
        AssignmentViewReader,
        RaterListReader,
        MyQueueReader,
        RatingsSummaryData,
        ExperimentStatisticsData,
        InvestigationRollupData,
        DatasetData,
    )
    for port in read_ports:
        assert "commit" not in port.__dict__, port.__name__
        assert "rollback" not in port.__dict__, port.__name__
