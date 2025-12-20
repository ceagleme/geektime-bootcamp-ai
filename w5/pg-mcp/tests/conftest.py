"""Pytest configuration and shared fixtures.

This module provides shared fixtures and configuration for all tests.
"""

import pytest

from pg_mcp.config.settings import reset_settings


@pytest.fixture(autouse=True)
def reset_config() -> None:
    """Reset global settings before each test."""
    reset_settings()
