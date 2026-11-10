"""Export tutoring pack manifests to disk."""

from app.db.session import SessionLocal
from app.domains.artefacts.core.domain.types import ArtefactType
from app.domains.artefacts.core.infrastructure.artefact_store import ArtefactStore
from app.domains.artefacts.core.infrastructure.models import Artefact


def main() -> None:
    store = ArtefactStore()
    with SessionLocal() as session:
        packs = (
            session.query(Artefact)
            .filter(Artefact.artefact_type == ArtefactType.POST_CLASS_REVIEW_PACK.value)
            .all()
        )
        for pack in packs:
            refs = store.export_review_pack(pack.artefact_id, pack.manifest)
            pack.artefact_refs = refs
        session.commit()


if __name__ == "__main__":
    main()
