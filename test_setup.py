from clients.supabase_client import SupabaseClient
from clients.notion_client import NotionClientWrapper
from clients.gemini_client import GeminiClient
from config.settings import settings

print("Testing Kandy AI Setup...\n")

# Test Supabase
try:
    supabase = SupabaseClient()
    users = supabase.fetch('users', limit=1)
    print(f"✅ Supabase: Connected ({len(users)} users)")
except Exception as e:
    print(f"❌ Supabase: {e}")

# Test Notion
try:
    notion = NotionClientWrapper()
    pages = notion.query_database()
    print(f"✅ Notion: Connected ({len(pages)} pages)")
except Exception as e:
    print(f"❌ Notion: {e}")

# Test Gemini
try:
    gemini = GeminiClient()
    response = gemini.generate_completion(
        system_prompt='You are brief.',
        user_prompt='Say "test"'
    )
    print(f"✅ Gemini: Connected")
except Exception as e:
    print(f"❌ Gemini: {e}")

print("\nSetup test complete!")
