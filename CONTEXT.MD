# Project Blueprint: AI-Driven Hashtag Generator ("PulseTag")

## 1. Project Overview & Architecture
**Objective:** Build a web application that takes a social media post URL (LinkedIn or X/Twitter), parses the text content, and uses an LLM to generate high-value, trending hashtags. The user can then "inject" these hashtags into the text and copy the result.

**Tech Stack:**
* **Frontend:** Next.js 14 (App Router), Tailwind CSS, Lucide React (icons).
* **Backend:** Python 3.11+, FastAPI.
* **Scraping:** Playwright (Headless Browser) + BeautifulSoup4.
* **AI:** OpenAI API (GPT-4o) or Anthropic API (Claude 3.5).
* **Containerisation:** Docker & Docker Compose.

---

## 2. Implementation Prompts (Copy & Paste these into the AI Agent)

### Phase 1: Infrastructure Scaffolding
**Prompt:**
> Act as a Senior DevOps Engineer. I need to scaffold a new full-stack application.
>
> 1.  **Structure:** Create a root directory containing two folders: `/frontend` and `/backend`.
> 2.  **Backend:** Initialize a Python FastAPI project. Include a `requirements.txt` with: `fastapi`, `uvicorn`, `playwright`, `beautifulsoup4`, `openai`, `python-dotenv`.
> 3.  **Frontend:** Initialize a Next.js 14 project using TypeScript and Tailwind CSS.
> 4.  **Docker:** Create a root `docker-compose.yml` that runs the backend on port 8000 and the frontend on port 3000. Ensure the backend mounts the local directory for hot-reloading.
> 5.  **Action:** Create these files and verify I can start the stack.

---

### Phase 2: The Scraper ("The Eyes")
**Prompt:**
> Act as a Python Automation Specialist. We need to build the scraping logic in the Backend.
>
> 1.  **Setup:** Create a file `backend/scraper.py`.
> 2.  **Logic:** Implement a class `SocialScraper`.
>     * Use `async_playwright` to launch a chromium browser.
>     * **Function `extract_text(url: str)`:** Navigate to the URL. Wait for the DOM to load.
>     * **Heuristics:** If the URL is LinkedIn, look for the main post body class (inspect common LinkedIn classes or extract all text from `<article>`). If X (Twitter), extract text from the tweet container.
>     * **Bot Evasion:** Set a realistic User-Agent. Add a random delay (1-3 seconds) before extraction.
>     * **Cookie Bypass (Crucial):** Check for an environment variable `LINKEDIN_COOKIES`. If present, inject these cookies into the browser context before navigating. This is necessary to bypass login walls.
> 3.  **Action:** Write the code and handle errors gracefully (e.g., if the post is private).

---

### Phase 3: The Intelligence ("The Brain") & API
**Prompt:**
> Act as a Backend API Developer. We need to connect the scraper to the AI and expose an endpoint.
>
> 1.  **AI Service:** Create `backend/ai_engine.py`. Initialize the OpenAI client.
> 2.  **The Prompt:** Create a function `analyze_post(text_content)`. Use the specific System Prompt defined below (see "Viral System Prompt").
> 3.  **API Endpoint:** In `backend/main.py`, create a POST endpoint `/api/analyze`.
>     * **Input:** JSON `{ "url": "..." }`
>     * **Process:** Call `scraper.extract_text(url)` -> get text. Call `ai_engine.analyze_post(text)` -> get hashtags.
>     * **Output:** Return a JSON object with `{ "original_text": "...", "hashtags": { "safe": [], "rising": [], "niche": [] } }`.
> 4.  **Action:** Implement the route and the AI logic.

#### **Viral System Prompt (For use in Step 2 above):**
> "You are a Viral Social Media Strategist. You analyse social media posts to maximise reach.
>
> **Input:** The text content of a user's post.
> **Task:** Analyse the core topics, tone, and industry.
> **Output:** Return ONLY a JSON object with three arrays of hashtags:
> 1.  **'safe':** High-volume, broad tags (e.g., #Marketing, #Tech). Use these for baseline visibility.
> 2.  **'rising':** Trending, mid-volume tags relevant *right now* or to specific modern sub-cultures (e.g., #GenAI, #GrowthHacking).
> 3.  **'niche':** Specific, low-competition tags that target high-intent users (e.g., #SaaSMarketingTips).
>
> **Rules:**
> * Do not include the # symbol in the string, just the word.
> * Ensure tags are CamelCase (e.g., 'DigitalMarketing', not 'digitalmarketing').
> * Do not return any conversational text, only the JSON."

---

### Phase 4: The Frontend UI ("The Editor")
**Prompt:**
> Act as a React Frontend Developer. Build the UI in `frontend/app/page.tsx`.
>
> 1.  **Layout:** A centred, modern card layout.
>     * **Top:** An input field "Paste Post URL" and a "Generate Tags" button.
> 2.  **Editor State:**
>     * Create a text area that displays the `original_text` returned from the API. Make this editable.
> 3.  **Hashtag Pills:**
>     * Below the text area, display the three categories (Safe, Rising, Niche) in distinct columns or colour-coded groups.
>     * **Interactivity:** When a user clicks a hashtag 'pill', it should append that hashtag (with a #) to the end of the text area content automatically. Disable/grey out the pill after clicking.
> 4.  **Export:**
>     * Add a "Copy to Clipboard" button that copies the final state of the text area.
> 5.  **Action:** Build the components and connect them to the backend API.

---

## 3. How to Setup & Test (User Guide)

Once the AI has generated the code, follow these steps to run it:

### 1. Configure Secrets
Create a `.env` file in the `/backend` folder:
```bash
OPENAI_API_KEY=sk-proj-... (your key here)
# Optional: If LinkedIn blocks the scraper, log in to LinkedIn on Chrome,
# use a plugin to "Get cookies.txt", and format them for Playwright here.
LINKEDIN_COOKIES=...