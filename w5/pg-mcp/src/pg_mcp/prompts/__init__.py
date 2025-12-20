"""Prompt templates and builders for LLM interactions.

This module provides prompt templates and utility functions for generating
prompts used in natural language to SQL conversion.
"""

from pg_mcp.prompts.sql_generation import (
    SQL_GENERATION_SYSTEM_PROMPT,
    build_user_prompt,
)

__all__ = [
    "SQL_GENERATION_SYSTEM_PROMPT",
    "build_user_prompt",
]
