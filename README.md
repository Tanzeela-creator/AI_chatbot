# 🤖 AI Chatbot

A web-based AI chatbot developed as an internship project.

The chatbot allows users to communicate with an AI assistant through text and voice input. It also provides optional voice output, conversation history, Markdown responses, error handling, and a responsive web interface.


## 🚀 Live Demo

Vercel: https://ai-chatbot-iidd.vercel.app/

## 📂 GitHub Repository

https://github.com/Tanzeela-creator/AI_chatbot

---

## ✨ Features

### Day 1 — Basic AI Chatbot

- User text input
- AI-generated responses
- AI API integration
- Web-based chatbot interface

### Day 2 — Chatbot Development

- Proper API integration
- Loading state while AI is responding
- Error handling
- Input validation
- Clean and responsive interface
- Custom system prompt defining the chatbot's role and behavior

### Day 3 — Chatbot Improvements

- Conversation history
- Clear Chat functionality
- Improved system prompt
- Markdown-formatted AI responses
- Secure Markdown rendering using DOMPurify
- Better user interface
- Input validation
- API error handling
- Voice input using browser Speech Recognition
- Optional voice output using browser Speech Synthesis
- Responsive design for mobile and desktop

---

## 🛠️ Technologies Used

- HTML5
- CSS3
- JavaScript
- Python
- Groq API
- `openai/gpt-oss-20b`
- Vercel
- Git
- GitHub
- Marked.js
- DOMPurify
- Web Speech API

---

## 🔌 API Integration

The chatbot uses the Groq API to generate AI responses.

The frontend sends the conversation history to the backend API endpoint:

```text
/api