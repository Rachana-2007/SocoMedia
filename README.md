# 🚀 SoCoMeDiA — AI Social Media Creative Director & Content OS

<p align="center">
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=FastAPI&logoColor=white" alt="FastAPI" />
  <img src="https://img.shields.io/badge/Groq_LLM-f34f29?style=for-the-badge&logo=openai&logoColor=white" alt="Groq LLM" />
  <img src="https://img.shields.io/badge/Hindsight_Memory-635BFF?style=for-the-badge&logo=brain&logoColor=white" alt="Hindsight Memory" />
  <img src="https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white" alt="Tailwind CSS" />
  <img src="https://img.shields.io/badge/Python_3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
</p>

---

## 📌 Overview

**SoCoMeDiA** is an AI-powered Social Media Creative Director and Content Operating System designed to automate high-performing social media campaigns, Gen-Z viral adaptations, artwork prompts, and global content localizations.

Powered by **Groq's high-speed LLM engine** and **Hindsight Vector Memory API**, SoCoMeDiA retains past post analytics, campaign records, and engagement patterns to continuously improve hook generation, tone matching, and strategy recommendation.

---

## ✨ Key Features

### 🧠 1. Long-Term Hindsight Memory Bank
* **Memory Recall**: Recalls past top-performing posts, successful hooks, and platform-specific formats before drafting content.
* **Continuous Learning**: Retains new post records and engagement metrics to adapt to evolving audience preferences.
* **Seeding Pipeline**: Built-in script (`seed_memory.py`) to bulk ingest historical post analytics (`social_media_history.json`).

### ⚡ 2. AI Post Generator & Creative Director
* Multi-platform optimization (**Instagram, LinkedIn, X/Twitter, TikTok, YouTube**).
* Custom tone selection (*Engaging & Viral, Professional, High Energy, Tech, Gen-Z*).
* Generates formatted captions, strategic memory insights, visual artwork prompts, and optimized hashtag clusters.

### 🔥 3. Gen-Z Viral Engine & Slang Converter (`/genzify`)
* Adapts standard copy into hyper-viral Gen-Z internet slang across customizable intensity tiers:
  * 🟢 **Mild**: Tasteful slang (*low-key, vibe check, bet, valid*).
  * 🟡 **Hype**: Authentic viral slang (*no cap fr fr, it's giving, ate and left no crumbs, rent free*).
  * 🔴 **Brainrot**: Maximum chaotic internet culture (*skibidi, rizz, fanum tax, mogging, mewing, cooked*).
* Outputs slang definitions and vibe breakdowns.

### 🎨 4. AI Poster & Artwork Prompt Generator (`/generate-image-prompt`)
* Creates rich visual generation prompts for **Midjourney**, **Stable Diffusion**, and **DALL-E**.
* Recommends cohesive color palettes, visual concept direction, poster headlines, and subheadlines.

### 🌐 5. Multilingual Translation & Cultural Localizer (`/translate`)
* Translates content across global languages while preserving social media cadence, emojis, slang intent, and hashtags.

### 💻 6. Modern Studio Workspace (Frontend)
* Single-page dark/light mode interactive workspace.
* Live post preview cards, copy-to-clipboard actions, memory reasoning inspect drawer, and real-time backend API integration.

---

## 🏗️ Project Architecture & Directory Structure

```
SoCoMeDiA/
├── index.html                  # Sleek Web Studio Frontend (Tailwind CSS, Lucide Icons)
├── seed_memory.py              # Hindsight Memory Seeding Script
├── social_media_history.json   # Historical post dataset & performance benchmarks
├── socomedia-agent/
│   └── backend/
│       ├── main.py             # FastAPI Server & AI Endpoints (Groq + Hindsight)
│       └── .env                # API Keys & Environment Configuration
└── README.md                   # Project Documentation
```

---

## 🛠️ Tech Stack

| Component | Technology |
| :--- | :--- |
| **Backend API** | [FastAPI](https://fastapi.tiangolo.com/), Uvicorn, Pydantic |
| **LLM Inference** | [Groq API](https://groq.com/) (`openai/gpt-oss-120b` / LLaMA models) |
| **Vector Memory Engine** | [Hindsight API](https://api.hindsight.vectorize.io) (`hindsight-client`) |
| **Frontend UI** | HTML5, Tailwind CSS, Space Grotesk & Inter Fonts, Lucide Icons, Canvas Confetti |
| **Data Format** | JSON / REST Endpoints |

---

## 🚀 Quick Start & Installation

### 1️⃣ Prerequisites
Ensure you have Python 3.10+ installed and active API keys for:
* **Groq API Key**: [Get Groq API Key](https://console.groq.com/)
* **Hindsight API Key**: [Get Hindsight API Key](https://api.hindsight.vectorize.io)

---

### 2️⃣ Backend Setup & Server Execution

Navigate to the backend directory and install dependencies:

```bash
cd socomedia-agent/backend

# Create virtual environment (optional but recommended)
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
# source venv/bin/activate

# Install required packages
pip install fastapi uvicorn hindsight-client groq pydantic
```

Set environment variables or update `socomedia-agent/backend/.env`:
```env
HINDSIGHT_API_KEY=your_hindsight_api_key_here
GROQ_API_KEY=your_groq_api_key_here
```

Run the FastAPI server:
```bash
uvicorn main:app --reload --port 8000
```
> The backend server will start at `http://localhost:8000`. API documentation is available at `http://localhost:8000/docs`.

---

### 3️⃣ Seed Long-Term Memory (Optional but Recommended)

Seed historical campaign data into the Hindsight vector bank:

```bash
# Run from the project root directory
python seed_memory.py
```

---

### 4️⃣ Launch Web Frontend

Open `index.html` directly in your browser or run a simple local web server:

```bash
# Python HTTP Server
python -m http.server 3000

# Or using npx
npx serve .
```

Access the studio at `http://localhost:3000` (or open `index.html` in Chrome/Firefox/Edge).

---

## 📡 API Endpoints Summary

| Method | Endpoint | Description |
| :---: | :--- | :--- |
| `POST` | `/generate-post` | Recalls memory from Hindsight & generates post, reasoning, Gen-Z variant, and image prompt |
| `POST` | `/genzify` | Converts text into Gen-Z slang with configurable intensity (`mild`, `hype`, `brainrot`) |
| `POST` | `/translate` | Translates post into target language with cultural localization |
| `POST` | `/generate-image-prompt` | Creates 3D/poster image generation prompt and visual layout suggestions |
| `POST` | `/save-post` | Saves post record & engagement metrics back to the Hindsight memory bank |

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the issues page or submit a pull request.

---

## 📄 License

This project is licensed under the MIT License.
