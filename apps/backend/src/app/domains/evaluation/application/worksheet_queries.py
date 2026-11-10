"""Named H1 and H2 worksheet rendering queries."""

from __future__ import annotations

from app.domains.evaluation.application.packet_detail_queries import (
    get_h1_packet_detail,
    get_h2_packet_detail,
)
from app.domains.evaluation.application.packet_ports import (
    H1PacketDetailDependencies,
    H2PacketDetailDependencies,
)
from app.domains.evaluation.application.worksheet_html.h2_renderer import (
    render_h2_worksheet_html_pdf,
)
from app.domains.evaluation.application.worksheet_html.renderer import (
    render_h1_worksheet_html_pdf,
)


async def generate_h1_worksheet(
    dependencies: H1PacketDetailDependencies,
    *,
    evaluation_packet_id: str,
    rater_id: str,
) -> tuple[bytes, str]:
    detail = await get_h1_packet_detail(
        dependencies,
        evaluation_packet_id=evaluation_packet_id,
        rater_id=rater_id,
    )
    packet_code = str(detail.get("packet_code") or evaluation_packet_id)
    return render_h1_worksheet_html_pdf(detail), f"{packet_code}-worksheet.pdf"


async def generate_h2_worksheet(
    dependencies: H2PacketDetailDependencies,
    *,
    evaluation_packet_id: str,
    rater_id: str,
) -> tuple[bytes, str]:
    detail = await get_h2_packet_detail(
        dependencies,
        evaluation_packet_id=evaluation_packet_id,
        rater_id=rater_id,
    )
    packet_code = str(detail.get("packet_code") or evaluation_packet_id)
    return render_h2_worksheet_html_pdf(detail), f"{packet_code}-h2-worksheet.pdf"
