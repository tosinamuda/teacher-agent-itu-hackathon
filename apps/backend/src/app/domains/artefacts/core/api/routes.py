from fastapi import APIRouter

from app.domains.artefacts.types.lesson_plan.api.routes import router as lesson_plan_router
from app.domains.artefacts.types.post_class_review_pack.api.routes import (
    router as post_class_review_pack_router,
)

router = APIRouter(tags=["artefacts"])
router.include_router(lesson_plan_router)
router.include_router(post_class_review_pack_router)
