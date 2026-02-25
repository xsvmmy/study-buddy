# StudyBuddy — AI-Powered Study Chatbot

A beginner-friendly AI chatbot that lets you upload study documents (PDF or TXT)
and ask questions about them. Built with Python, Flask, and the OpenAI API.

This project is designed to teach:
- How to get and use an OpenAI API key
- How to connect Python code to an external API
- How to deploy a web app using Replit

---

## What It Does

1. **Upload documents** — Drop in a PDF or TXT file (lecture notes, textbooks, study guides)
2. **Ask questions** — Chat with the AI about the material
3. **Get answers** — The AI reads your documents and answers based on the content

---

## File Structure

```
study-bot/
├── main.py              ← The Flask web server (all the backend logic lives here)
├── config.py            ← Where YOU put your OpenAI API key
├── requirements.txt     ← List of Python packages to install
├── .replit              ← Tells Replit how to run the app
├── README.md            ← This documentation file
└── templates/
    └── index.html       ← The chat UI (HTML + CSS + JavaScript)
```

### What each file does

| File | Purpose |
|------|---------|
| `config.py` | **Start here.** Put your API key and settings here. |
| `main.py` | The Flask server. Handles document uploads, chat messages, and calls the OpenAI API. |
| `templates/index.html` | The complete chat interface — HTML, CSS, and JavaScript in one file. |
| `requirements.txt` | Lists the Python packages Flask needs. Run `pip install -r requirements.txt` to install them. |
| `.replit` | Tells Replit to run `python main.py` when you click the Run button. |

---

## Step 1 — Get an OpenAI API Key

You need an API key to let the app talk to OpenAI's AI models.

1. Go to [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)
2. Sign up for a free OpenAI account (or log in)
3. Click **"+ Create new secret key"**
4. Give it a name (e.g., "StudyBuddy") and click **Create**
5. **Copy the key immediately** — it starts with `sk-...` and OpenAI only shows it once

> **Note on costs:** OpenAI's API is not completely free, but it is very cheap for
> personal use. GPT-3.5-turbo costs roughly $0.002 per 1,000 tokens (~750 words).
> A typical study session costs a fraction of a cent. New accounts also get free
> trial credits.

---

## Option A — Run Locally

### Prerequisites

- Python 3.9 or newer installed on your computer
- A terminal / command prompt

### Setup

**1. Install dependencies**

Open a terminal in the project folder and run:
```bash
pip install -r requirements.txt
```

**2. Add your API key**

Open `config.py` in any text editor. Find this line:
```python
OPENAI_API_KEY = "your-api-key-here"
```
Replace `"your-api-key-here"` with your actual key:
```python
OPENAI_API_KEY = "sk-abc123..."
```
Save the file.

**3. Start the server**

```bash
python main.py
```

You should see:
```
==================================================
  StudyBuddy is running!
  Open http://localhost:5000 in your browser
==================================================
```

**4. Open the app**

Go to [http://localhost:5000](http://localhost:5000) in your browser.

---

## Option B — Deploy on Replit (Recommended for Sharing)

Replit is a free, browser-based coding platform. It lets you run and share
web apps without installing anything on your computer.

### Step-by-Step Replit Deployment

#### 1. Create a Replit account
Go to [https://replit.com](https://replit.com) and sign up for a free account.

#### 2. Create a new Repl
- Click the **"+ Create Repl"** button (top left)
- Choose **"Import from GitHub"** if your project is on GitHub, OR
- Choose **"Python"** as the template to start a blank Python Repl

#### 3. Upload your project files
If you chose a blank Python Repl:
- In the left sidebar, click the **Files** icon (looks like a folder)
- Upload all the project files:
  - `main.py`
  - `config.py`
  - `requirements.txt`
  - `.replit`
- Create the `templates` folder and upload `templates/index.html` inside it

#### 4. Add your API key using Replit Secrets
Replit Secrets are a secure way to store API keys — they're hidden from anyone
who views your code.

- In the left sidebar, click the **"Secrets"** icon (looks like a lock 🔒)
  - It may also be under the **Tools** menu
- Click **"+ New Secret"**
- Set **Key** to: `OPENAI_API_KEY`
- Set **Value** to: your actual API key (e.g., `sk-abc123...`)
- Click **"Add Secret"**

> **Why use Secrets instead of config.py on Replit?**
> If you share your Repl publicly, anyone can see `config.py` — and your API key.
> Replit Secrets are encrypted and not visible in the code editor.
> The app automatically reads the secret from the environment, so nothing else
> needs to change.

#### 5. Install dependencies
Replit usually installs packages from `requirements.txt` automatically.
If it doesn't, open the **Shell** tab (bottom of screen) and run:
```bash
pip install -r requirements.txt
```

#### 6. Run the app
Click the big green **"Run"** button at the top of the screen.

Replit will:
1. Install any missing packages
2. Start the Flask server (`python main.py`)
3. Open a **Webview** panel showing your app

#### 7. Use the app
The Webview shows the app running at a URL like:
```
https://studybuddy.your-username.repl.co
```

You can share this URL with anyone!

> **Replit free plan note:** Free Repls go to "sleep" after a period of inactivity
> and wake up when someone visits the URL. The first load may take ~10 seconds.

---

## How to Use StudyBuddy

### Uploading a document
1. Click the **📚 Documents** button (or the hamburger ☰ menu on mobile)
2. Click **"Choose File"** and select a PDF or TXT file
   - Or drag and drop a file onto the upload area
3. You'll see the document name appear in the sidebar with a confirmation message in the chat

### Asking questions
1. Type your question in the text box at the bottom
2. Press **Enter** or click the send button (↑)
3. The AI will answer based on your uploaded documents

### Example questions
- "Summarize the main points of this document"
- "What does the document say about [topic]?"
- "Explain [concept] in simple terms"
- "Create 5 quiz questions from this material"
- "What are the key differences between X and Y?"

### Managing documents
- Click **✕** next to a document name to remove it
- Click **"Clear Chat & Documents"** to start a fresh session

---

## Changing Settings

Open `config.py` to adjust:

```python
# Switch to GPT-4o for better answers (requires GPT-4 access on your account)
MODEL = "gpt-4o"

# Increase how much of a large document the AI can see at once
MAX_DOC_CHARS = 12000
```

---

## Troubleshooting

### "OpenAI API key is not set"
- Make sure you edited `config.py` and replaced `"your-api-key-here"` with your real key
- On Replit, check that you added the `OPENAI_API_KEY` secret correctly

### "Invalid API key"
- Double-check that you copied the full key (it starts with `sk-`)
- Make sure there are no extra spaces before or after the key

### "No readable text found" when uploading a PDF
- Some PDFs contain scanned images rather than real text
- Try copying text from the PDF manually — if you can't select/copy text in the PDF, it's a scanned image and won't work
- Use a TXT file instead, or find a different version of the document

### "Rate limit reached"
- You've sent too many requests in a short time
- Wait 30–60 seconds and try again
- Free/trial accounts have lower rate limits than paid accounts

### The app won't start
- Make sure you ran `pip install -r requirements.txt` first
- Check that you're using Python 3.9 or newer: `python --version`
- If port 5000 is in use, change the port in `main.py`:
  ```python
  app.run(host="0.0.0.0", port=8080, debug=True)
  ```

---

## How the Code Works (for curious beginners)

```
User types a message in the browser
         ↓
JavaScript sends it to /chat (Flask route in main.py)
         ↓
main.py builds a prompt:
  - System message: "You are StudyBuddy. Here is the document: ..."
  - Chat history: the last 10 messages
  - New message: what the user just typed
         ↓
main.py sends the prompt to OpenAI's API
         ↓
OpenAI returns the AI's response
         ↓
main.py sends the response back to the browser as JSON
         ↓
JavaScript adds the response as a chat bubble in the UI
```

### Key concepts this project demonstrates

| Concept | Where to see it |
|---------|----------------|
| API keys | `config.py`, top of `main.py` |
| REST API calls | `/chat` route in `main.py` |
| File uploads | `/upload` route in `main.py` |
| Browser sessions | `get_session_id()` in `main.py` |
| Responsive CSS | Media queries in `templates/index.html` |
| Fetch API (JavaScript) | `sendMessage()` in `templates/index.html` |
| Markdown rendering | `renderMarkdown()` in `templates/index.html` |

---

## Tech Stack

| Tool | What it does |
|------|-------------|
| [Flask](https://flask.palletsprojects.com/) | Python web framework — handles HTTP requests |
| [OpenAI Python SDK](https://github.com/openai/openai-python) | Connects to GPT models via the API |
| [pypdf](https://pypdf.readthedocs.io/) | Extracts text from PDF files |
| [marked.js](https://marked.js.org/) | Renders Markdown in the browser |
| [Replit](https://replit.com/) | Free cloud platform for running and sharing the app |
