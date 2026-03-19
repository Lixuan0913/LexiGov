## ⚙️ Setup Guide

Follow these steps to run the ASEAN Multilingual AI Assistant locally.

---

### 🧊 Quick Setup (All-in-One)

```bash
# 1️⃣ Clone the Repository
git clone https://github.com/your-username/your-repo.git
cd LexiGov

# 2️⃣ Install Dependencies
pip install -r requirements.txt

# 3️⃣ Create .env file
# (add the following inside .env)
GOOGLE_API_KEY=your_google_api_key
HF_TOKEN=your_huggingface_token
GOOGLE_APPLICATION_CREDENTIALS=./credentials.json

# 4️⃣ Run the Server
python app.py

# 5️⃣ Open in Browser
http://localhost:5000
