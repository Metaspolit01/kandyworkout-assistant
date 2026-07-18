"""
Seed script: inserts the default user and initial data into Supabase.
Safe to run multiple times — skips inserts if data already exists.

Requires SUPABASE_SERVICE_KEY (service_role key) to bypass Row Level Security.
Add it as a GitHub Actions secret: Settings → Secrets → SUPABASE_SERVICE_KEY

Usage:
    python -m database.seed
"""

from datetime import date

from supabase import create_client, Client
from config.settings import settings
from config.logger import logger


def _get_admin_client() -> Client:
    """Create a Supabase client using the service_role key to bypass RLS."""
    key = settings.SUPABASE_SERVICE_KEY or settings.SUPABASE_KEY
    if not settings.SUPABASE_SERVICE_KEY:
        logger.warning(
            "SUPABASE_SERVICE_KEY is not set — falling back to anon key. "
            "Inserts may fail due to Row Level Security. "
            "Add SUPABASE_SERVICE_KEY (service_role key) as a GitHub Actions secret."
        )
    return create_client(settings.SUPABASE_URL, key)


def seed():
    db = _get_admin_client()

    # ── 1. Upsert user ────────────────────────────────────────────────────────
    existing = db.table("users").select("*").ilike("name", settings.USER_NAME).limit(1).execute()

    if existing.data:
        user = existing.data[0]
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
        result = db.table("users").insert(user_data).execute()
        user = result.data[0]
        logger.info(f"Created user '{settings.USER_NAME}' (id={user['id']})")

    user_id = user["id"]

    # ── 2. Coach memory: initial level ────────────────────────────────────────
    existing_memory = (
        db.table("coach_memory")
        .select("id")
        .eq("user_id", user_id)
        .eq("key", "current_level")
        .limit(1)
        .execute()
    )
    if existing_memory.data:
        logger.info("Coach memory 'current_level' already exists. Skipping.")
    else:
        db.table("coach_memory").insert({
            "user_id": user_id,
            "memory_type": "progression",
            "key": "current_level",
            "value": {"push": "beginner", "pull": "beginner", "legs": "beginner", "core": "beginner"},
            "confidence": 1.0,
        }).execute()
        logger.info("Created initial coach memory.")

    # ── 3. Initial body measurement ───────────────────────────────────────────
    today = date.today().isoformat()
    existing_measurement = (
        db.table("body_measurements")
        .select("id")
        .eq("user_id", user_id)
        .eq("date", today)
        .limit(1)
        .execute()
    )
    if existing_measurement.data:
        logger.info("Body measurement for today already exists. Skipping.")
    else:
        db.table("body_measurements").insert({
            "user_id": user_id,
            "date": today,
            "weight_kg": float(settings.USER_WEIGHT_KG),
        }).execute()
        logger.info("Created initial body measurement.")

    # ── 4. Welcome achievement ────────────────────────────────────────────────
    existing_achievement = (
        db.table("achievements")
        .select("id")
        .eq("user_id", user_id)
        .eq("title", "Welcome Aboard")
        .limit(1)
        .execute()
    )
    if existing_achievement.data:
        logger.info("Welcome achievement already exists. Skipping.")
    else:
        db.table("achievements").insert({
            "user_id": user_id,
            "title": "Welcome Aboard",
            "description": "Started your calisthenics journey with Kandy AI",
            "category": "consistency",
            "achieved_date": today,
            "icon": "🚀",
        }).execute()
        logger.info("Created 'Welcome Aboard' achievement.")

    logger.info("✅ Seed completed successfully.")


if __name__ == "__main__":
    seed()

