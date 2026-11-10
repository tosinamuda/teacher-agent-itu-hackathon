"""Compose the review-pack study with the product's live generators."""

from app.domains.artefacts.types.post_class_review_pack.infrastructure.generation_wiring import (
    build_base_review_pack_generator,
    build_review_pack_personaliser,
)
from app.domains.experiments.infrastructure.sqlalchemy_experiment_store import (
    open_experiment_store,
)

from .h1.experiment import H1Experiment
from .h2.experiment import H2Experiment


def build_h1_experiment() -> H1Experiment:
    return H1Experiment(
        generator=build_base_review_pack_generator(),
        open_store=open_experiment_store,
    )


def build_h2_experiment() -> H2Experiment:
    return H2Experiment(
        personaliser=build_review_pack_personaliser(),
        open_store=open_experiment_store,
    )
