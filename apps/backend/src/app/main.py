"""The backend API: ``uvicorn app.main:app`` serves the ``app`` built here.

The environment is prepared before anything else is imported, because the database
engine and the model clients read it as they load.
"""

from app.environment import prepare_environment

prepare_environment()

from app.server import create_app  # noqa: E402

app = create_app()
