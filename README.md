## ⚙️ Setup Guide

Follow these steps to run the ASEAN Multilingual AI Assistant locally.

---

### 🧊 Quick Setup (All-in-One)


<div style="border:1px solid #ccc; padding:10px; margin:10px 0; border-radius:6px;">
<b>1️⃣ Clone the Repository</b><br>
git clone https://github.com/your-username/your-repo.git  
cd LexiGov
</div>

<div style="border:1px solid #ccc; padding:10px; margin:10px 0; border-radius:6px;">
<b>2️⃣ Install Dependencies</b><br>
pip install -r requirements.txt
</div>

<div style="border:1px solid #ccc; padding:10px; margin:10px 0; border-radius:6px;">
<b>3️⃣ Create .env file</b><br>
GOOGLE_API_KEY=your_google_api_key  
HF_TOKEN=your_huggingface_token  
GOOGLE_APPLICATION_CREDENTIALS=./credentials.json
</div>

<div style="border:1px solid #ccc; padding:10px; margin:10px 0; border-radius:6px;">
<b>4️⃣ Run the Server</b><br>
python app.py
</div>

<div style="border:1px solid #ccc; padding:10px; margin:10px 0; border-radius:6px;">
<b>5️⃣ Open in Browser</b><br>
http://localhost:5000
</div>
