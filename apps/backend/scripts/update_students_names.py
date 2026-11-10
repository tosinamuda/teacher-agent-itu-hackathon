import asyncio
import random

from sqlalchemy import select, update

from app.db.session import AsyncSessionLocal
from app.domains.artefacts.core.infrastructure.models import ArtefactPlan
from app.domains.assessments.models import ExitTicketSubmission
from app.domains.learners.models import LearnerProfile

# Nigerian Names Dataset
NIGERIAN_NAMES = {
    "Yoruba": [
        ("Ade", "Adeyemi"),
        ("Bolu", "Balogun"),
        ("Tosin", "Adeleke"),
        ("Femi", "Otedola"),
        ("Tayo", "Ayeni"),
        ("Seyi", "Makinde"),
        ("Funke", "Akindele"),
        ("Kemi", "Adeosun"),
        ("Yemi", "Osinbajo"),
        ("Bola", "Tinubu"),
        ("Remi", "Tinubu"),
        ("Babajide", "Sanwo-Olu"),
        ("Folake", "Coker"),
        ("Kunle", "Afolayan"),
        ("Tiwa", "Savage"),
        ("Wizkid", "Balogun"),
        ("Davido", "Adeleke"),
        ("Burna", "Ogulu"),
        ("Simi", "Ogunleye"),
        ("Falz", "Falana"),
    ],
    "Igbo": [
        ("Chinedu", "Ikedieze"),
        ("Nkechi", "Blessing"),
        ("Emeka", "Ihedioha"),
        ("Chioma", "Chukwuka"),
        ("Obi", "Ezekwesili"),
        ("Ngozi", "Okonjo-Iweala"),
        ("Peter", "Obi"),
        ("Chukwuma", "Soludo"),
        ("Oby", "Ezekwesili"),
        ("Chimamanda", "Adichie"),
        ("Chinua", "Achebe"),
        ("Flavour", "Nabania"),
        ("Phyno", "Azubuike"),
        ("P-Square", "Okoye"),
        ("Don", "Jazzy"),
        ("Genevieve", "Nnaji"),
        ("Rita", "Dominic"),
        ("Pete", "Edochie"),
        ("Osita", "Iheme"),
        ("Kanayo", "Kanayo"),
    ],
    "Hausa": [
        ("Aminu", "Tambuwal"),
        ("Nasir", "El-Rufai"),
        ("Atiku", "Abubakar"),
        ("Muhammadu", "Buhari"),
        ("Aisha", "Buhari"),
        ("Sanusi", "Lamido"),
        ("Umar", "Ganduje"),
        ("Rabiu", "Kwankwaso"),
        ("Shehu", "Sani"),
        ("Fatima", "Dangote"),
        ("Aliko", "Dangote"),
        ("Abdulsamad", "Rabiu"),
        ("Hadiza", "Bala-Usman"),
        ("Zainab", "Ahmed"),
        ("Sadiya", "Farouq"),
        ("Ali", "Nuhu"),
        ("Rahama", "Sadau"),
        ("Nuhu", "Ribadu"),
        ("Mansur", "Dan-Ali"),
        ("Boss", "Mustapha"),
    ],
}


async def update_students() -> None:
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(LearnerProfile))
        learners = result.scalars().all()

        updated_count = 0
        used_codes = set()

        print(f"Found {len(learners)} learners to update.")

        all_names = []
        for tribe in NIGERIAN_NAMES.values():
            all_names.extend(tribe)

        random.shuffle(all_names)

        for i, learner in enumerate(learners):
            first, last = all_names[i % len(all_names)]

            base_code = f"{first.lower()}-{last.lower()}"
            code = base_code
            counter = 1
            while code in used_codes:
                code = f"{base_code}-{counter}"
                counter += 1

            used_codes.add(code)

            old_id = learner.student_id
            new_id = code
            new_name = f"{first} {last}"

            print(f"Updating {learner.full_name} ({old_id}) -> {new_name} ({new_id})")

            learner.full_name = new_name
            learner.student_id = new_id

            await session.execute(
                update(ExitTicketSubmission)
                .where(ExitTicketSubmission.student_id == old_id)
                .values(student_id=new_id)
            )
            await session.execute(
                update(ArtefactPlan)
                .where(ArtefactPlan.student_id == old_id)
                .values(student_id=new_id)
            )

            updated_count += 1

        await session.commit()
        print(f"Successfully updated {updated_count} learners.")


if __name__ == "__main__":
    try:
        asyncio.run(update_students())
    except Exception as e:
        print(f"Error: {e}")
