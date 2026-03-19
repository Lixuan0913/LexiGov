## ⚙️ Setup Guide

Follow these steps to run the ASEAN Multilingual AI Assistant locally.

---

### 📋 Prerequisites

Make sure you have installed:

- Python 3.10+
- pip (Python package manager)

---

### 📥 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/your-repo.git
cd LexiGov

### 2️⃣ Install Dependencies
```bash
pip install -r requirements.txt

###🔑 3️⃣ Set Up Environment Variables
Create a .env file in the root directory:
```bash
GOOGLE_API_KEY=your_google_api_key
HF_TOKEN=your_huggingface_token
GOOGLE_APPLICATION_CREDENTIALS=./credentials.json

###🚀4️⃣ Running the Server
```bash
python app.py
The backend should now be running at: http://localhost:10000

