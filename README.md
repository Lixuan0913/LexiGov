## ⚙️ Setup Guide

Follow these steps to run the ASEAN Multilingual AI Assistant locally.

---

### 🧊 Quick Setup (All-in-One)

<div style="border:1px solid #ccc; padding:12px; margin:12px 0; border-radius:6px;">
<b>1️⃣ Clone the Repository</b><br>
<pre>
git clone https://github.com/your-username/your-repo.git
cd LexiGov
</pre>
</div>

<div style="border:1px solid #ccc; padding:12px; margin:12px 0; border-radius:6px;">
<b>2️⃣ Install Dependencies</b><br>
<pre>
pip install -r requirements.txt
</pre>
</div>

<div style="border:1px solid #ccc; padding:12px; margin:12px 0; border-radius:6px;">
<b>3️⃣ Create .env File</b><br>
Add the following inside <code>.env</code>:  
<pre>
GOOGLE_API_KEY=your_google_api_key
HF_TOKEN=your_huggingface_token
GOOGLE_APPLICATION_CREDENTIALS=./credentials.json
</pre>
</div>

<div style="border:1px solid #ccc; padding:12px; margin:12px 0; border-radius:6px;">
<b>4️⃣ Run the Server</b><br>
<pre>
python app.py
</pre>
</div>

<div style="border:1px solid #ccc; padding:12px; margin:12px 0; border-radius:6px;">
<b>5️⃣ Open in Browser</b><br>
<pre>
http://localhost:5000
</pre>
</div>
