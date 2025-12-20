"""Database connection pool management.

This module provides utilities for creating and managing asyncpg connection
pools for PostgreSQL databases.
"""

import asyncpg
from asyncpg import Pool

from pg_mcp.config.settings import DatabaseConfig


async def create_pool(config: DatabaseConfig) -> Pool:
    """Create a connection pool for a single database.

    Args:
        config: Database configuration containing connection parameters
            and pool settings.

    Returns:
        Pool: An asyncpg connection pool instance.

    Raises:
        asyncpg.PostgresError: If connection to the database fails.

    Example:
        >>> config = DatabaseConfig(host="localhost", name="mydb")
        >>> pool = await create_pool(config)
        >>> async with pool.acquire() as conn:
        ...     result = await conn.fetch("SELECT 1")
    """
    pool = await asyncpg.create_pool(
        host=config.host,
        port=config.port,
        database=config.name,
        user=config.user,
        password=config.password,
        min_size=config.min_pool_size,
        max_size=config.max_pool_size,
        timeout=config.pool_timeout,
        command_timeout=config.command_timeout,
    )

    if pool is None:
        raise RuntimeError(f"Failed to create connection pool for {config.name}")

    return pool


async def create_pools(configs: list[DatabaseConfig]) -> dict[str, Pool]:
    """Create connection pools for multiple databases.

    This function creates pools concurrently for all provided database
    configurations.

    Args:
        configs: List of database configurations.

    Returns:
        dict[str, Pool]: Dictionary mapping database names to their pools.

    Raises:
        asyncpg.PostgresError: If any database connection fails.

    Example:
        >>> configs = [
        ...     DatabaseConfig(name="db1", host="localhost"),
        ...     DatabaseConfig(name="db2", host="localhost"),
        ... ]
        >>> pools = await create_pools(configs)
        >>> assert "db1" in pools and "db2" in pools
    """
    pools: dict[str, Pool] = {}

    for config in configs:
        pool = await create_pool(config)
        pools[config.name] = pool

    return pools


async def close_pools(pools: dict[str, Pool]) -> None:
    """Close all connection pools gracefully.

    This function closes all pools and waits for all connections to be
    released properly.

    Args:
        pools: Dictionary mapping database names to their pools.

    Example:
        >>> pools = await create_pools(configs)
        >>> # ... use pools ...
        >>> await close_pools(pools)
    """
    for pool in pools.values():
        await pool.close()
