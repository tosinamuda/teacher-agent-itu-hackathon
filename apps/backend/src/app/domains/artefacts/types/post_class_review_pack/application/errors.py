"""Why a revision note cannot be built or checked."""


class MissingPackInputError(Exception):
    """An input a revision note is built from cannot be found; the message names which."""


class StudentPackGenerationError(MissingPackInputError):
    """Raised when a student's pack cannot be generated."""
