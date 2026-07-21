from app.core.config import settings

print("\n========== CONFIG TEST ==========\n")

print(f"App Name: {settings.APP_NAME}")
print(f"Environment: {settings.ENVIRONMENT}")

if settings.GEMINI_API_KEY:
    print("✅ Gemini API Key Loaded Successfully")
    print(f"Key starts with: {settings.GEMINI_API_KEY[:8]}...")
else:
    print("❌ Gemini API Key Not Found")