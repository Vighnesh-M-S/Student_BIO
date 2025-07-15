# 🧠 Student Manager with AI Summarizer (Flask + Ollama + Frontend)

This project is a full-stack application that allows you to manage students with CRUD operations and generate AI-based summaries using the `gemma3:1b` model from [Ollama](https://ollama.com).

## 🌐 Deployed Link: [AWS_StudentAPP](http://13.61.179.181:5000/)

## 🚀 Features

- Create, Read, Update, and Delete student records
- Generate AI summaries of student profiles via Ollama + Gemma 3B model
- Beautiful HTML/CSS/JS frontend
- Flask backend with REST API
- Deployed on AWS EC2 (works with Gunicorn + Ollama)

---

## 🏗 Project Structure

```
Student_BIO/
├── app.py               # Flask backend
├── templates/
│   └── index.html       # HTML frontend
├── static/
│   ├── styles.css       # CSS
│   └── script.js        # JavaScript
├── server.log           # Logs from Gunicorn
├── ollama.log           # Logs from Ollama (optional)
└── requirements.txt     # Python dependencies
```

---

## ⚙️ API Endpoints

| Method | Endpoint                      | Description                   |
|--------|-------------------------------|-------------------------------|
| POST   | `/students`                   | Add a new student             |
| GET    | `/students`                   | Get all students              |
| GET    | `/students/<id>`              | Get a student by ID           |
| PUT    | `/students/<id>`              | Update a student by ID        |
| DELETE | `/students/<id>`              | Delete a student by ID        |
| GET    | `/students/<id>/summary`      | AI-generated summary via Ollama |

---

## 🧪 Example cURL Commands

Add a new student:
```bash
curl -X POST http://<server-ip>:5000/students   -H "Content-Type: application/json"   -d '{"name": "Alice", "age": 21, "email": "alice@example.com"}'
```

Get summary:
```bash
curl http://<server-ip>:5000/students/1/summary
```

---

## 🌐 Deployment Guide (AWS EC2)

### 1. Launch EC2 Ubuntu Instance (t3.medium or higher)

### 2. Clone and set up project

```bash
sudo apt update && sudo apt install -y python3-pip python3-venv curl git
python3 -m venv stu
source stu/bin/activate
pip install flask flask-cors requests gunicorn
```

### 3. Install Ollama

```bash
curl -fsSL https://ollama.com/install.sh | sh
nohup ollama serve > ollama.log 2>&1 &
ollama run gemma3:1b
```

### 4. Run the App

```bash
nohup gunicorn -b 0.0.0.0:5000 app:app > server.log 2>&1 &
```

---

## ✅ Notes

- Make sure port 5000 is open in EC2 security group
- Use `systemd` or `tmux` for auto-start on reboot (optional)
- Ollama must be running for summary generation

---
