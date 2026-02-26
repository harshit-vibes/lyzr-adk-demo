# Lyzr ADK — Learn to Build AI Agents

[![PyPI](https://img.shields.io/pypi/v/lyzr-adk)](https://pypi.org/project/lyzr-adk/)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/harshit-vibes/lyzr-adk-demo/blob/master/notebooks/01_getting_started.ipynb)
[![Tests](https://img.shields.io/badge/tests-13%2F13%20passing-brightgreen)](validate.py)

In 15 hands-on lessons you'll go from writing your first agent to building a WhatsApp Business co-pilot and a multi-agent e-commerce support system — all with [lyzr-adk](https://pypi.org/project/lyzr-adk/). Every notebook runs locally or in one click on Google Colab. All 15 lessons are fully validated and working.

---

## Learning Path

```
🟢 Lessons 1–3    →    🟡 Lessons 4–8    →    🔴 Lessons 9–10    →    🚀 Bonus 14–15
  First agent          Memory, tools,          Guardrails +            WhatsApp +
                       RAG, contexts            Capstone              Multi-agent
```

---

## What You'll Learn

- Create AI agents using 20+ LLMs (OpenAI, Anthropic, Google, Groq, and more)
- Build agents with conversational memory and multi-turn sessions
- Add custom Python tools your agent can call
- Ground agents in your own documents with RAG (Retrieval-Augmented Generation)
- Inject dynamic context (user profiles, company info, live data)
- Add safety guardrails: toxicity detection, PII protection, prompt injection prevention
- Generate structured, type-safe outputs with Pydantic models
- Stream responses in real time
- Generate images with DALL-E 3 and Gemini

---

## Prerequisites

- Python 3.8+
- A Lyzr API key — sign up free at [lyzr.ai](https://lyzr.ai)

---

## Quick Start

**Option A — Run locally:**
```bash
git clone https://github.com/harshit-vibes/lyzr-adk-demo.git
cd lyzr-adk-demo
pip install -r requirements.txt
cp .env.example .env        # add your LYZR_API_KEY
jupyter notebook
```

**Option B — Run on Google Colab:**
Click any "Open in Colab" badge in the lesson table below — no setup required.

---

## Lessons

### Core Series (Lessons 1–10)

| # | Notebook | Topic | Difficulty | Time | Open |
|---|----------|--------|------------|------|------|
| 1 | [01_getting_started.ipynb](notebooks/01_getting_started.ipynb) | Hello, Agent! — Studio setup, create agent, run | 🟢 Beginner | 15 min | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/harshit-vibes/lyzr-adk-demo/blob/master/notebooks/01_getting_started.ipynb) |
| 2 | [02_providers_and_models.ipynb](notebooks/02_providers_and_models.ipynb) | LLM Providers — OpenAI, Anthropic, Google, Groq | 🟢 Beginner | 20 min | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/harshit-vibes/lyzr-adk-demo/blob/master/notebooks/02_providers_and_models.ipynb) |
| 3 | [03_agent_lifecycle.ipynb](notebooks/03_agent_lifecycle.ipynb) | Agent Management — list, retrieve, update, clone, delete | 🟢 Beginner | 20 min | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/harshit-vibes/lyzr-adk-demo/blob/master/notebooks/03_agent_lifecycle.ipynb) |
| 4 | [04_structured_outputs.ipynb](notebooks/04_structured_outputs.ipynb) | Structured Outputs — type-safe responses with Pydantic | 🟡 Intermediate | 25 min | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/harshit-vibes/lyzr-adk-demo/blob/master/notebooks/04_structured_outputs.ipynb) |
| 5 | [05_memory_and_sessions.ipynb](notebooks/05_memory_and_sessions.ipynb) | Memory & Sessions — multi-turn conversations | 🟡 Intermediate | 25 min | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/harshit-vibes/lyzr-adk-demo/blob/master/notebooks/05_memory_and_sessions.ipynb) |
| 6 | [06_tools_and_functions.ipynb](notebooks/06_tools_and_functions.ipynb) | Custom Tools — Python functions as agent tools | 🟡 Intermediate | 30 min | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/harshit-vibes/lyzr-adk-demo/blob/master/notebooks/06_tools_and_functions.ipynb) |
| 7 | [07_knowledge_bases_rag.ipynb](notebooks/07_knowledge_bases_rag.ipynb) | RAG — knowledge bases, document ingestion, retrieval | 🟡 Intermediate | 30 min | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/harshit-vibes/lyzr-adk-demo/blob/master/notebooks/07_knowledge_bases_rag.ipynb) |
| 8 | [08_contexts.ipynb](notebooks/08_contexts.ipynb) | Dynamic Contexts — inject background info into agents | 🟡 Intermediate | 20 min | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/harshit-vibes/lyzr-adk-demo/blob/master/notebooks/08_contexts.ipynb) |
| 9 | [09_rai_guardrails.ipynb](notebooks/09_rai_guardrails.ipynb) | Responsible AI — toxicity, PII, topic filters | 🔴 Advanced | 30 min | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/harshit-vibes/lyzr-adk-demo/blob/master/notebooks/09_rai_guardrails.ipynb) |
| 10 | [10_capstone_project.ipynb](notebooks/10_capstone_project.ipynb) | Capstone — full research assistant (all features) | 🔴 Advanced | 45 min | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/harshit-vibes/lyzr-adk-demo/blob/master/notebooks/10_capstone_project.ipynb) |

### Optional Advanced Lessons

| # | Notebook | Topic | Difficulty | Time | Open |
|---|----------|--------|------------|------|------|
| 11 | [11_streaming.ipynb](notebooks/11_streaming.ipynb) | Streaming — real-time token-by-token responses | 🔴 Advanced | 20 min | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/harshit-vibes/lyzr-adk-demo/blob/master/notebooks/11_streaming.ipynb) |
| 12 | [12_image_and_file_generation.ipynb](notebooks/12_image_and_file_generation.ipynb) | Image Generation — DALL-E 3 and Gemini image models | 🔴 Advanced | 25 min | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/harshit-vibes/lyzr-adk-demo/blob/master/notebooks/12_image_and_file_generation.ipynb) |
| 13 | [13_advanced_features.ipynb](notebooks/13_advanced_features.ipynb) | Advanced Features — reflection, bias check, groundedness | 🔴 Advanced | 25 min | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/harshit-vibes/lyzr-adk-demo/blob/master/notebooks/13_advanced_features.ipynb) |

### Bonus Lessons

| # | Notebook | Topic | Difficulty | Time | Open |
|---|----------|--------|------------|------|------|
| 14 | [14_whatsapp_business_copilot.ipynb](notebooks/14_whatsapp_business_copilot.ipynb) | WhatsApp Co-pilot — Meta Cloud API + lyzr-adk agent | 🔴 Advanced | 35 min | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/harshit-vibes/lyzr-adk-demo/blob/master/notebooks/14_whatsapp_business_copilot.ipynb) |
| 15 | [15_multi_agent_ecommerce.ipynb](notebooks/15_multi_agent_ecommerce.ipynb) | Multi-agent — manager routes to 3 specialist sub-agents | 🔴 Advanced | 35 min | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/harshit-vibes/lyzr-adk-demo/blob/master/notebooks/15_multi_agent_ecommerce.ipynb) |

---

## Project Structure

```
lyzr-adk-demo/
├── notebooks/
│   ├── 01_getting_started.ipynb
│   ├── 02_providers_and_models.ipynb
│   ├── ...
│   ├── 13_advanced_features.ipynb
│   ├── 14_whatsapp_business_copilot.ipynb
│   └── 15_multi_agent_ecommerce.ipynb
├── .env.example          # Copy to .env and add your API key
├── requirements.txt
├── LICENSE
└── README.md
```

---

## Each Notebook Follows the Same Structure

Every lesson is self-contained and follows a consistent layout:
1. **Overview** — what you'll learn and why it matters
2. **Setup** — install, import, initialize (runs fresh every time)
3. **Concepts** — one concept at a time, explanation + working code
4. **Common Mistake** — shows what goes wrong and why
5. **Exercise** — hands-on practice with starter scaffold
6. **Summary** — quick-reference API table
7. **Next Steps** — link to the next lesson

---

## Resources

- **Documentation**: [docs.lyzr.ai](https://docs.lyzr.ai)
- **PyPI**: [pypi.org/project/lyzr-adk](https://pypi.org/project/lyzr-adk/)
- **Community**: [discord.gg/lyzr](https://discord.gg/lyzr)
- **Issues**: [GitHub Issues](https://github.com/harshit-vibes/lyzr-adk-demo/issues)

---

## Contributing

Contributions are welcome! To add a lesson or fix an issue:

1. Fork the repository
2. Create a branch: `git checkout -b feat/lesson-name`
3. Follow the notebook schema above
4. Open a pull request

Please ensure every code cell runs top-to-bottom without errors.

---

## License

MIT — see [LICENSE](LICENSE).
