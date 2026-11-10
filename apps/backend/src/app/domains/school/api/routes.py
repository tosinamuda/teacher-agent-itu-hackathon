"""School routes."""

from __future__ import annotations

import uuid
from typing import NoReturn

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.deps import get_db
from app.domains.school.application import SchoolApplicationError, SchoolApplicationService
from app.domains.school.application.workspace_provisioning_service import (
    WorkspaceProvisioningApplicationService,
)
from app.domains.school.schemas import (
    ClassResponse,
    SchoolCreateRequest,
    SchoolResponse,
    SchoolSetupCatalogResponse,
    SchoolUpdateRequest,
    SchoolWorkspaceCreateRequest,
    SchoolWorkspaceResponse,
    SubjectOfferingCatalogResponse,
    SubjectSlotRulesResponse,
    TeacherCreateRequest,
    TeacherOptionResponse,
)
from app.shared.auth import Actor
from app.shared.authz import requires

router = APIRouter(prefix="/school", tags=["school"])


def _raise_http_error(error: SchoolApplicationError) -> NoReturn:
    raise HTTPException(status_code=error.status_code, detail=error.detail)


@router.get("/classes", response_model=list[ClassResponse])
async def list_classes(
    grade: str | None = None,
    school_id: uuid.UUID | None = None,
    db: AsyncSession = Depends(get_db),
) -> list[ClassResponse]:
    service = SchoolApplicationService()
    return await service.list_classes(db=db, grade=grade, school_id=school_id)


@router.get("/schools", response_model=list[SchoolResponse])
async def list_schools(
    db: AsyncSession = Depends(get_db),
) -> list[SchoolResponse]:
    service = SchoolApplicationService()
    return await service.list_schools(db=db)


@router.post("/schools", response_model=SchoolResponse)
async def create_school(
    payload: SchoolCreateRequest,
    db: AsyncSession = Depends(get_db),
    _actor: Actor = Depends(requires(obj="school:*", act="create")),
) -> SchoolResponse:
    service = SchoolApplicationService()
    try:
        return await service.create_school(db=db, payload=payload)
    except SchoolApplicationError as error:
        _raise_http_error(error)


@router.post("/teachers", response_model=TeacherOptionResponse)
async def create_teacher(
    payload: TeacherCreateRequest,
    db: AsyncSession = Depends(get_db),
    _actor: Actor = Depends(requires(obj="auth/user:*", act="create")),
) -> TeacherOptionResponse:
    """Onboard a teacher (research-manager only) so they can be assigned a workspace."""
    from app.domains.users.application.service import (
        UserAlreadyExistsError,
        UserApplicationService,
    )

    try:
        teacher = await UserApplicationService().create_user(
            db=db,
            code=payload.code,
            email=payload.email,
            full_name=payload.full_name,
            role="teacher",
        )
    except UserAlreadyExistsError as error:
        raise HTTPException(status_code=409, detail=str(error)) from None
    return TeacherOptionResponse(
        id=teacher.id,
        full_name=teacher.full_name,
        auth_id=teacher.auth_id,
        email=teacher.email,
    )


@router.get("/schools/{school_id}", response_model=SchoolResponse)
async def get_school(
    school_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
) -> SchoolResponse:
    service = SchoolApplicationService()
    try:
        return await service.get_school(db=db, school_id=school_id)
    except SchoolApplicationError as error:
        _raise_http_error(error)


@router.patch("/schools/{school_id}", response_model=SchoolResponse)
async def update_school(
    school_id: uuid.UUID,
    payload: SchoolUpdateRequest,
    db: AsyncSession = Depends(get_db),
    _actor: Actor = Depends(requires(obj="school:*", act="update")),
) -> SchoolResponse:
    service = SchoolApplicationService()
    try:
        return await service.update_school(db=db, school_id=school_id, payload=payload)
    except SchoolApplicationError as error:
        _raise_http_error(error)


@router.get("/setup/catalog", response_model=SchoolSetupCatalogResponse)
async def get_school_setup_catalog(
    db: AsyncSession = Depends(get_db),
) -> SchoolSetupCatalogResponse:
    service = SchoolApplicationService()
    return await service.list_setup_catalog(db=db)


@router.get("/setup/workspaces", response_model=list[SchoolWorkspaceResponse])
async def list_school_setup_workspaces(
    school_id: uuid.UUID | None = None,
    db: AsyncSession = Depends(get_db),
) -> list[SchoolWorkspaceResponse]:
    service = SchoolApplicationService()
    return await service.list_workspaces(db=db, school_id=school_id)


@router.post("/setup/workspaces", response_model=SchoolWorkspaceResponse)
async def create_school_setup_workspace(
    payload: SchoolWorkspaceCreateRequest,
    db: AsyncSession = Depends(get_db),
    _actor: Actor = Depends(requires(obj="workspace:*", act="create")),
) -> SchoolWorkspaceResponse:
    service = WorkspaceProvisioningApplicationService()
    try:
        return await service.create_workspace(db=db, payload=payload)
    except SchoolApplicationError as error:
        _raise_http_error(error)


@router.get("/subject-offerings", response_model=SubjectOfferingCatalogResponse)
async def get_subject_offerings() -> SubjectOfferingCatalogResponse:
    catalog = SchoolApplicationService().subject_offering_catalog()
    return SubjectOfferingCatalogResponse(
        curriculum=catalog.curriculum,
        subject_slots=SubjectSlotRulesResponse(
            total_subjects=catalog.subject_slots.total_subjects,
            compulsory_subjects=catalog.subject_slots.compulsory_subjects,
            field_core_subjects=catalog.subject_slots.field_core_subjects,
            trade_subjects=catalog.subject_slots.trade_subjects,
            notes=list(catalog.subject_slots.notes),
        ),
        core_compulsory_subjects=list(catalog.core_compulsory_subjects),
        fields_of_study=dict(catalog.fields_of_study),
        trade_subjects=list(catalog.trade_subjects),
    )
