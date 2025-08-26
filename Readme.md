# ✨ AI Productivity Architect ✨

An **AI-powered productivity assistant** that takes your tasks, goals, and schedule — then architects your day/week into a personalized plan using proven productivity frameworks (Pomodoro ⏳, Eisenhower Matrix 🗂, Deep Work 💡, etc.).

⚡ **In one line:** An AI that doesn’t just suggest tasks, but actually structures your day into a working plan.

---

## 🌟 Features

* 🖥️ **CLI-based AI assistant** (Phase 1)
* ⏳ Task input with deadlines, preferences, and available time
* 📑 AI-generated structured plans in JSON / tabular format
* 📚 **RAG** (Retrieval-Augmented Generation) for productivity best practices
* 🔗 Function calling → Google Calendar, Notion, Trello (later phase)
* 🎨 Beautiful CLI tables & colors with **Rich**
* 🌐 Extendable to a **React frontend** with animations later

---

## 🛠️ Tech Stack

### Core

* 🐍 **Python 3.10+**
* ⚡ **Typer** → CLI framework
* 🎨 **Rich** → Pretty CLI tables and colors

### AI Layer

* 🤖 **OpenAI API** / **Groq API** (LLM)
* 🧠 **ChromaDB** → Vector database for RAG

### Storage

* 🗄️ **SQLite** → Task history & settings

### Integrations (later)

* 📆 **Google Calendar API**
* 📝 **Notion/Trello API**

### Frontend (Phase 2+)

* 🚀 **FastAPI** (backend APIs)
* 🎨 **React + TailwindCSS** (frontend UI)
* 📊 **Recharts/D3.js** (visualizations + animations)

---

## 🚀 Roadmap

### 🎯 Phase 1: CLI MVP

* [ ] Setup Python environment
* [ ] Build CLI with Typer
* [ ] Accept tasks, time, preferences
* [ ] Call LLM (OpenAI/Groq) with structured prompts
* [ ] Return JSON plan
* [ ] Display plan in Rich table

### 📚 Phase 2: RAG Integration

* [ ] Setup ChromaDB with productivity frameworks
* [ ] Add context retrieval for better AI plans

### 💾 Phase 3: Storage + Function Calling

* [ ] Store plans in SQLite
* [ ] Add Google Calendar sync
* [ ] Add Notion/Trello task sync

### 🎨 Phase 4: Frontend with Animations

* [ ] Expose backend with FastAPI
* [ ] Build React frontend (task input + charts)
* [ ] Add animated charts, smooth transitions
* [ ] Deploy (Vercel + Render)

---

## 📦 Installation

```bash
# Clone the repo
git clone https://github.com/yourusername/ai-productivity-architect.git
cd ai-productivity-architect

# Create virtual env
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt
```

---

## 🖥️ Usage

### CLI Example

```bash
python planner.py plan --tasks "Study React, Gym, Interview Prep" --time "9-6" --user student


---

## 🤝 Contributing

PRs are welcome! Open an issue first to discuss what you’d like to change.

---

## 📜 License

MIT License

---
