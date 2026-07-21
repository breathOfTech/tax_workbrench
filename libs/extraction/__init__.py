"""Extraction library — structured fact extraction from user messages."""

from libs.extraction.log_formatter import format_extraction_result, log_extraction_result
from libs.extraction.schema import ExtractionResult, ExtractedFact, FactAction
from libs.extraction.service import extract_from_message

__all__ = [
    "ExtractionResult",
    "ExtractedFact",
    "FactAction",
    "extract_from_message",
    "format_extraction_result",
    "log_extraction_result",
]
