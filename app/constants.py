from enum import StrEnum


class InputType(StrEnum):
    TEXT = "Text"
    PDF = "PDF Upload"
    BULK = "Bulk Upload"


MIN_CLASSIFICATION_SCORE = 0.92
