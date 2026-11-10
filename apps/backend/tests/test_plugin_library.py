"""The plugin library: plugins on hand that are not installed until someone adds one."""

from __future__ import annotations

from app.domains.content.plugins.library import in_library, library_plugin


def test_the_library_holds_the_flashcards_plugin_as_a_valid_plugin() -> None:
    plugin = library_plugin("flashcards")

    assert plugin is not None
    assert [p.name for p in plugin.plugins] == ["flashcards"]
    assert plugin.plugins[0].definition is not None
    assert plugin.plugins[0].definition.label == "Flashcards"
    assert plugin.description.startswith("Flashcards on each lesson objective")


def test_a_folder_is_found_by_its_name_and_never_by_a_path() -> None:
    assert library_plugin("../plugins/class-test") is None
    assert library_plugin("no-such-plugin") is None
    assert "flashcards" in {plugin.folder for plugin in in_library()}
