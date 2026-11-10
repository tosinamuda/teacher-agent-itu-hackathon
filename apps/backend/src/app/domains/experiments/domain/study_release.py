"""Where the published MSc study lives on the Hugging Face Hub."""

HUB_OWNER = "tosinamuda"


def hub_repo(dataset: str) -> str:
    """The dataset's Hub repository id, e.g. ``tosinamuda/ng-jss1-math-lesson-plans``."""
    return f"{HUB_OWNER}/{dataset}"
