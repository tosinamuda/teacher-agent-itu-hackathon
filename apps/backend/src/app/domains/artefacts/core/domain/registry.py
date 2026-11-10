"""The content types an instantiation can generate, one specification each."""

from __future__ import annotations

from collections.abc import Iterable

from app.domains.artefacts.core.domain.specification import ContentSpecification


class ContentRegistry:
    """Every registered kind, keyed by its stored kind, in registration order."""

    def __init__(self, specifications: Iterable[ContentSpecification] = ()) -> None:
        self._specifications: dict[str, ContentSpecification] = {}
        for specification in specifications:
            self.register(specification)

    def register(self, specification: ContentSpecification) -> None:
        if specification.kind in self._specifications:
            raise ValueError(f"content_already_registered:{specification.kind}")
        self._specifications[specification.kind] = specification

    def specification(self, kind: str) -> ContentSpecification:
        try:
            return self._specifications[kind]
        except KeyError as exc:
            raise ValueError(f"unknown_content:{kind}") from exc

    def kinds(self) -> tuple[str, ...]:
        return tuple(self._specifications)

    def __contains__(self, kind: object) -> bool:
        """Whether ``kind`` is registered."""
        return kind in self._specifications
