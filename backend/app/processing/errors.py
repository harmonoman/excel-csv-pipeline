"""
errors.py — Shared pipeline exception types.

Kept in a separate module to avoid circular imports between
pipeline.py (which orchestrates stages) and stage modules
(like schema.py) that need to raise PipelineError.
"""


class PipelineError(Exception):
    """
    Raised when any pipeline stage fails.

    Preserves the originating stage name, exception type, and message
    so callers can return structured error responses without losing context.
    """

    def __init__(self, stage: str, error_type: str, error_message: str):
        self.stage = stage
        self.error_type = error_type
        self.error_message = error_message
        super().__init__(
            f"Pipeline failed at stage '{stage}': [{error_type}] {error_message}"
        )