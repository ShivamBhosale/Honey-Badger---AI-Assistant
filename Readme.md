# HoneyBadger AI 🦡

## Overview

HoneyBadger AI is a reliability-focused, debate-driven GenAI system built with Streamlit and Ollama.

Unlike typical AI chat applications that blindly return model output, Honey Badger AI evaluates, critiques, refines, and validates responses before showing them to the user.

It is designed around one principle:

> AI output must earn trust before being displayed.

---

## Core Philosophy

Honey Badger AI does not trust the first answer.

Every response goes through:

1. Initial generation  
2. AI-based critique  
3. Revision pass  
4. Rule-based evaluation  
5. Confidence scoring  
6. Guardrail approval  

Only high-confidence answers are shown.

---

## Architecture

- User Question 
↓
- Generator (gemma3)
↓
- Text-Based Critic
↓
- Revised Answer
↓
- Rule Evaluation
↓
- Score Fusion
↓
- Guardrails
↓
- Final Output


---

## Models

- **Generator**: `gemma3:latest`
- **Critic**: Text-based evaluation (same model)
- Fully local execution via **Ollama**

No API keys required.

---

## Features

- Text + optional image input
- Two-pass debate refinement
- AI-based critique scoring
- Rule-based evaluation checks
- Combined confidence score
- Guardrail-based rejection system
- Modern styled Streamlit interface
- Fully local inference

---

## Confidence System

Final score is calculated as:


If the final score meets the threshold → answer is approved.  
If not → the system rejects the answer.

This prevents low-quality or uncertain responses from being shown.

---

## Tech Stack

- Python
- Streamlit
- Ollama
- Requests

---

## Installation

### 1. Install Ollama
Download from: https://ollama.com

### 2. Pull the model
```bash
ollama pull gemma3:latest

pip install -r requirements.txt

ollama serve
streamlit run app.py

http://localhost:8501

How It Works

- User submits a question (optionally with an image)
- Generator produces an initial answer
- Critic evaluates clarity, relevance, and confidence
- Generator revises the answer based on critique
- Rule-based evaluation checks length, vagueness, and structure
- Scores are combined
- Guardrails decide whether to approve or reject

Why Honey Badger AI?

Most AI apps optimize for speed and fluency.

Honey Badger AI optimizes for:

- Reliability
- Evaluation
- Controlled output
- Multi-stage reasoning
- Guardrail enforcement

It demonstrates production-style GenAI system design rather than simple prompt engineering.

Future Enhancements

- Confidence calibration tuning
- Auto-retry refinement loop
- Lightweight critic model
- Evaluation dashboard
- Tool integration
- Conversation memory

Status

Working prototype with debate refinement, scoring, guardrails, and styled UI.

