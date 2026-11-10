"""One-time script to migrate legacy student class_ids to proper UUIDs."""

import uuid

from dotenv import load_dotenv

load_dotenv()


from app.db.session import SessionLocal  # noqa: E402
from app.domains.learners.models import LearnerProfile  # noqa: E402


def migrate_class_ids() -> None:
    # Explicit mapping based on DB inspection
    class_mapping = {
        # Class A, SS1
        "SS1-A": uuid.UUID("c0253303-d361-4034-ad56-49341e9e5ebd"),
        # Class B, SS1
        "SS1-B": uuid.UUID("c9b50f84-418a-4dae-9939-d8a098752616"),
        # Fallback to Class B, SS1 (Class C not found)
        "SS1-C": uuid.UUID("c9b50f84-418a-4dae-9939-d8a098752616"),
    }

    with SessionLocal() as db:
        print("Starting migration of legacy class IDs...")

        learners = (
            db.query(LearnerProfile).filter(LearnerProfile.class_id.in_(class_mapping.keys())).all()
        )
        updated_count = 0

        for learner in learners:
            old_id = str(learner.class_id)
            if old_id in class_mapping:
                new_id = class_mapping[old_id]
                learner.class_id = new_id
                updated_count += 1

        if updated_count > 0:
            db.commit()
            print(f"Successfully migrated {updated_count} learners to valid UUIDs.")
        else:
            print("No learners found requiring migration.")


if __name__ == "__main__":
    migrate_class_ids()
