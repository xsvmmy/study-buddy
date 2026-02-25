# ============================================================
#  config.py — Developer Configuration
#  StudyBuddy AI Study Chatbot
# ============================================================
#
#  STEP 1: Get your OpenAI API key
#  --------------------------------
#  1. Go to: https://platform.openai.com/api-keys
#  2. Sign in or create a free OpenAI account
#  3. Click "+ Create new secret key"
#  4. Copy the key — it starts with "sk-..."
#  5. Paste it below, replacing "your-api-key-here"
#
#  IMPORTANT: Keep your API key private!
#  - Never share it publicly or commit it to GitHub
#  - If deploying to Replit, see README.md for how to use
#    Replit Secrets instead of putting the key directly here
#
# ============================================================

OPENAI_API_KEY = "your-api-key-here"

# ============================================================
#  Optional Settings (safe to leave as-is)
# ============================================================

# Which AI model to use.
# "gpt-3.5-turbo" works with most standard API keys (cheaper).
# "gpt-4o" gives better answers but costs more and requires
# an account with GPT-4 access.
MODEL = "gpt-3.5-turbo"

# Maximum number of characters from uploaded documents to send
# to the AI at once. Higher = AI sees more content but uses
# more tokens (and costs more). 8000 chars ≈ ~5 pages of text.
MAX_DOC_CHARS = 8000
