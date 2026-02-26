# ============================================================
#  main.py — StudyBuddy AI Study Chatbot
#  Built with Flask (Python web framework) + OpenAI API
# ============================================================
#
#  What this file does:
#  1. Starts a local web server using Flask
#  2. Serves the chat interface (templates/index.html)
#  3. Handles document uploads — extracts readable text from
#     PDF and TXT files
#  4. Handles chat messages — sends your question + document
#     content to OpenAI, and returns the AI's answer
#
#  Routes (URLs the server listens to):
#    GET  /           → Serve the main chat page
#    GET  /state      → Return current session data (for page reload)
#    POST /upload     → Accept a file upload, extract its text
#    POST /chat       → Accept a message, return AI response
#    POST /clear      → Clear the current session
#    POST /remove-doc → Remove one document from the session
#
# ============================================================

from flask import Flask, request, render_template, session, jsonify
import openai
import os
import io
import uuid

# File extensions we accept for image OCR
IMAGE_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp'}

# --- Load settings from config.py ---
# We try config.py first. If the key is the default placeholder
# or config.py is missing, we fall back to an environment variable.
# This lets the same code work locally (config.py) AND on Replit (Secrets).
try:
    from config import OPENAI_API_KEY, MODEL, MAX_DOC_CHARS
except ImportError:
    # config.py not found — use defaults
    OPENAI_API_KEY = ""
    MODEL = "gpt-3.5-turbo"
    MAX_DOC_CHARS = 8000

# If the config key is still the placeholder, check the OS environment
if not OPENAI_API_KEY or OPENAI_API_KEY == "your-api-key-here":
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")

# --- Set up the OpenAI client ---
# This object is how we talk to the OpenAI API
client = openai.OpenAI(api_key=OPENAI_API_KEY)

# --- Create the Flask web application ---
app = Flask(__name__)

# Flask uses a "secret key" to sign session cookies (browser storage).
# In production, use a long random string. For local use, the default is fine.
app.secret_key = os.environ.get("SECRET_KEY", "studybuddy-local-dev-secret")

# ============================================================
#  In-Memory Storage
# ============================================================
# We store each user's data in a Python dictionary.
# Key:   a unique session ID (stored in the user's browser cookie)
# Value: their uploaded documents and chat history
#
# NOTE: This resets when the server restarts — that's intentional
# for a simple study session. No database needed!
user_data = {}


# ============================================================
#  Helper Functions
# ============================================================

def get_session_id():
    """
    Get or create a unique ID for this browser session.
    Flask stores this ID in the user's cookie automatically.
    """
    if 'sid' not in session:
        session['sid'] = str(uuid.uuid4())  # e.g. "a3f2c1d8-..."
    return session['sid']


def get_user_data():
    """
    Get the current user's stored documents and chat history.
    Creates an empty record on first visit.
    """
    sid = get_session_id()
    if sid not in user_data:
        user_data[sid] = {
            'documents': [],  # List of {'name': str, 'text': str}
            'messages':  []   # List of {'role': str, 'content': str}
        }
    return user_data[sid]


def extract_text(file):
    """
    Read an uploaded file and return its text content as a string.

    Supports:
      - .txt files  (plain text, just read and decode)
      - .pdf files  (use pypdf to extract text from each page)

    Returns None if the file type is not supported.
    """
    filename = file.filename.lower()

    # --- Plain text files ---
    if filename.endswith('.txt'):
        raw_bytes = file.read()
        # decode() turns bytes into a Python string
        # errors='ignore' skips any characters that can't be decoded
        return raw_bytes.decode('utf-8', errors='ignore')

    # --- PDF files ---
    elif filename.endswith('.pdf'):
        try:
            from pypdf import PdfReader
            # Read the file into memory as bytes, then parse as PDF
            pdf = PdfReader(io.BytesIO(file.read()))
            pages = []
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:  # Some pages may be blank or image-only
                    pages.append(page_text)
            return "\n".join(pages).strip()
        except ImportError:
            return "Error: pypdf is not installed. Run: pip install pypdf"
        except Exception as e:
            return f"Error reading PDF: {str(e)}"

    # --- Image files (OCR via pytesseract + Pillow) ---
    elif filename.endswith(tuple(IMAGE_EXTENSIONS)):
        try:
            from PIL import Image
            import pytesseract
            # Open the image from the uploaded bytes
            img = Image.open(io.BytesIO(file.read()))
            # Convert to RGB so Tesseract can handle all formats (RGBA, palette, etc.)
            if img.mode not in ('RGB', 'L'):
                img = img.convert('RGB')
            # Run OCR — returns a string of all detected text
            text = pytesseract.image_to_string(img)
            # If Tesseract found nothing, return a note so the AI still knows an image was uploaded
            return text.strip() if text.strip() else "[No readable text detected in this image]"
        except ImportError:
            return (
                "Error: Image OCR requires Pillow and pytesseract.\n"
                "Run: pip install Pillow pytesseract\n"
                "Then install the Tesseract binary (brew install tesseract on macOS, "
                "or apt-get install tesseract-ocr on Ubuntu/Replit)."
            )
        except Exception as e:
            return f"Error reading image: {str(e)}"

    # --- Unsupported type ---
    else:
        return None


# ============================================================
#  Routes
# ============================================================

@app.route('/')
def index():
    """Serve the main chat page (templates/index.html)."""
    get_session_id()  # Initialize session on first visit
    return render_template('index.html')


@app.route('/state')
def get_state():
    """
    Return the current session's messages and document names as JSON.
    The frontend calls this when the page loads so it can restore
    the chat if the user refreshed the page.
    """
    data = get_user_data()
    return jsonify({
        'messages':  data['messages'],
        # Only send document names to the frontend (not the full text)
        'documents': [{'name': d['name']} for d in data['documents']]
    })


@app.route('/upload', methods=['POST'])
def upload():
    """
    Accept a file upload from the frontend.
    Extract its text, store it in the session, and return a summary.
    """
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']
    if not file.filename:
        return jsonify({'error': 'No file selected'}), 400

    # Check the file extension before processing
    ext = os.path.splitext(file.filename)[1].lower()
    allowed = {'.pdf', '.txt'} | IMAGE_EXTENSIONS
    if ext not in allowed:
        return jsonify({
            'error': f'Unsupported file type "{ext}". Please upload a PDF, TXT, or image file (PNG, JPG, etc.).'
        }), 400

    # Extract text from the file
    text = extract_text(file)

    if text is None:
        return jsonify({'error': 'Could not read this file type. Use PDF or TXT.'}), 400

    if not text.strip():
        is_image = ext in IMAGE_EXTENSIONS
        hint = 'Try a clearer photo.' if is_image else 'PDFs must contain real text (not scanned images).'
        return jsonify({'error': f'No readable text found. {hint}'}), 400

    # Truncate to MAX_DOC_CHARS to stay within OpenAI token limits
    truncated_text = text[:MAX_DOC_CHARS]
    was_truncated = len(text) > MAX_DOC_CHARS

    # Save to the user's session
    data = get_user_data()
    data['documents'].append({
        'name': file.filename,
        'text': truncated_text
    })

    return jsonify({
        'success':       True,
        'filename':      file.filename,
        'char_count':    len(text),
        'was_truncated': was_truncated,
        # A short preview to confirm the right content was read
        'preview':       text[:300] + ('...' if len(text) > 300 else '')
    })


@app.route('/chat', methods=['POST'])
def chat():
    """
    Accept a chat message from the user, call the OpenAI API,
    and return the AI's response.

    The uploaded document text is included in the system prompt
    so the AI can answer questions about it.
    """
    body = request.get_json() or {}
    user_message = body.get('message', '').strip()

    if not user_message:
        return jsonify({'error': 'Please enter a message'}), 400

    # Check that an API key has been configured
    if not OPENAI_API_KEY or OPENAI_API_KEY == "your-api-key-here":
        return jsonify({
            'error': 'OpenAI API key is not set. Open config.py and add your key.'
        }), 500

    data = get_user_data()

    # --- Build the system prompt ---
    # The system prompt tells the AI who it is and what context to use.
    if data['documents']:
        # Combine all uploaded document text into one context block
        doc_sections = []
        for doc in data['documents']:
            doc_ext = os.path.splitext(doc['name'])[1].lower()
            # Label image files so the AI knows this text came from OCR
            label = ' (OCR-extracted text from image)' if doc_ext in IMAGE_EXTENSIONS else ''
            doc_sections.append(f"=== {doc['name']}{label} ===\n{doc['text']}")
        doc_context = "\n\n".join(doc_sections)

        system_prompt = f"""You are StudyBuddy, a friendly and helpful AI study assistant.

The user has uploaded the following study material. Use it to answer their questions:

{doc_context}

Guidelines:
- Answer based on the uploaded documents when possible
- If a question isn't covered in the documents, say so, then give general help
- Keep answers clear and concise
- Use bullet points or numbered lists to organize longer answers
- Be encouraging and supportive"""

    else:
        # No documents uploaded yet — still be helpful
        system_prompt = """You are StudyBuddy, a friendly and helpful AI study assistant.

No documents have been uploaded yet. Help the user with their questions and gently remind them they can upload a PDF or TXT file to ask questions about specific study material.

Keep answers clear, concise, and encouraging."""

    # --- Build the message list for OpenAI ---
    # OpenAI expects a list of messages: system, then alternating user/assistant.
    # We include the last 10 messages for context (to keep API costs low).
    recent_history = data['messages'][-10:]

    openai_messages = [
        {"role": "system", "content": system_prompt},
        *recent_history,
        {"role": "user", "content": user_message}
    ]

    # --- Call the OpenAI API ---
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=openai_messages,
            max_tokens=1000  # Limit response length to control costs
        )
        ai_reply = response.choices[0].message.content.strip()

    except openai.AuthenticationError:
        return jsonify({
            'error': 'Invalid API key. Double-check the key in config.py.'
        }), 401

    except openai.RateLimitError:
        return jsonify({
            'error': 'Rate limit reached. Wait a moment and try again.'
        }), 429

    except openai.NotFoundError:
        return jsonify({
            'error': f'Model "{MODEL}" not found. Try changing MODEL to "gpt-3.5-turbo" in config.py.'
        }), 404

    except Exception as e:
        return jsonify({'error': f'AI error: {str(e)}'}), 500

    # --- Save this exchange to the session history ---
    data['messages'].append({'role': 'user',      'content': user_message})
    data['messages'].append({'role': 'assistant', 'content': ai_reply})

    return jsonify({'reply': ai_reply})


@app.route('/clear', methods=['POST'])
def clear():
    """Clear the user's chat history and all uploaded documents."""
    data = get_user_data()
    data['documents'] = []
    data['messages']  = []
    return jsonify({'success': True})


@app.route('/remove-doc', methods=['POST'])
def remove_doc():
    """Remove a single document from the session by name."""
    body = request.get_json() or {}
    doc_name = body.get('name', '')
    data = get_user_data()
    data['documents'] = [d for d in data['documents'] if d['name'] != doc_name]
    return jsonify({'success': True})


# ============================================================
#  Start the Server
# ============================================================
if __name__ == '__main__':
    # Read PORT from environment variables.
    # Replit and other platforms set this automatically.
    # Defaults to 5000 for local development.
    port = int(os.environ.get("PORT", 5000))

    print("\n" + "=" * 50)
    print("  StudyBuddy is running!")
    print(f"  Open http://localhost:{port} in your browser")
    print("=" * 50 + "\n")

    # host="0.0.0.0" makes the server accessible on your local network
    # debug=True gives helpful error messages during development
    app.run(host="0.0.0.0", port=port, debug=True)
