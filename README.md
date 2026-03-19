## ⚙️ Setup Guide

Follow these steps to run the ASEAN Multilingual AI Assistant locally.

---

### 📋 Prerequisites

- Python 3.10+
- pip (Python package manager)

---

```markdown
### 🧊 Quick Setup (All-in-One)

```bash
# Clone the Repository
git clone https://github.com/your-username/your-repo.git
cd LexiGov

# Install Dependencies
pip install -r requirements.txt

# Environment Variables (.env)
GOOGLE_API_KEY=your_google_api_key
HF_TOKEN=your_huggingface_token
GOOGLE_APPLICATION_CREDENTIALS=./credentials.json

# Run Server
python app.py

# Access
http://localhost:5000
