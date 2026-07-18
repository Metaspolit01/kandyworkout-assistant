"""
Seed script: inserts the default user and initial data into Supabase.
Safe to run multiple times — skips inserts if data already exists.

Usage:
    python -m database.seed
"""

from datetime import date

from clients.supabase_client import SupabaseClient
from config.settings import settings
from config.logger import logger


def seed():
    client = SupabaseClient()

    # ── 1. Upsert user ────────────────────────────────────────────────────────
    existing_users = client.fetch("users", filters={"name": settings.USER_NAME})

    if existing_users:
        user = existing_users[0]
        logger.info(f"User '{settings.USER_NAME}' already exists (id={user['id']}). Skipping insert.")
    else:
        user_data = {
            "name": settings.USER_NAME,
            "age": settings.USER_AGE,
            "height_cm": settings.USER_HEIGHT_CM,
            "weight_kg": float(settings.USER_WEIGHT_KG),
            "level": settings.USER_LEVEL,
            "goal": settings.USER_GOAL,
        }
        inserted = client.insert("users", user_data)
        user = inserted[0]
        logger.info(f"Created user '{settings.USER_NAME}' (id={user['id']})")

    user_id = user["id"]

    # ── 2. Coach memory: initial level ────────────────────────────────────────
    existing_memory = client.fetch(
        "coach_memory",
        filters={"user_id": user_id, "key": "current_level"}
    )
    if existing_memory:
        logger.info("Coach memory 'current_level' already exists. Skipping.")
    else:
        client.insert("coach_memory", {
            "user_id": user_id,
            "memory_type": "progression",
            "key": "current_level",
            "value": {"push": "beginner", "pull": "beginner", "legs": "beginner", "core": "beginner"},
            "confidence": 1.0,
        })
        logger.info("Created initial coach memory.")

    # ── 3. Initial body measurement ───────────────────────────────────────────
    today = date.today().isoformat()
    existing_measurement = client.fetch(
        "body_measurements",
        filters={"user_id": user_id, "date": today}
    )
    if existing_measurement:
        logger.info("Body measurement for today already exists. Skipping.")
    else:
        client.insert("body_measurements", {
            "user_id": user_id,
            "date": today,
            "weight_kg": float(settings.USER_WEIGHT_KG),
        })
        logger.info("Created initial body measurement.")

    # ── 4. Welcome achievement ────────────────────────────────────────────────
    existing_achievement = client.fetch(
        "achievements",
        filters={"user_id": user_id, "title": "Welcome Aboard"}
    )
    if existing_achievement:
        logger.info("Welcome achievement already exists. Skipping.")
    else:
        client.insert("achievements", {
            "user_id": user_id,
            "title": "Welcome Aboard",
            "description": "Started your calisthenics journey with Kandy AI",
            "category": "consistency",
            "achieved_date": today,
            "icon": "🚀",
        })
        logger.info("Created 'Welcome Aboard' achievement.")

    logger.info("✅ Seed completed successfully.")


if __name__ == "__main__":
    seed()
