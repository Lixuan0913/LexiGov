## 🚀 Live Demo

Skip the installation and try LexiGov directly in your browser! 

<div style="border:1px solid #0366d6; background-color: #f1f8ff; padding:12px; margin:12px 0; border-radius:6px;">
<b>🌐 Try the App Here:</b><br>
<a href="https://huggingface.co/spaces/kelly0913xuan/LexiGov" target="_blank" style="color: #0366d6; font-weight: bold; text-decoration: none;">Launch on Hugging Face Spaces ↗</a>
</div>

---

## ⚙️ Setup Guide

Follow these steps to run the ASEAN Multilingual AI Assistant locally.

### 🧊 Quick Setup (All-in-One)

<div style="border:1px solid #ccc; padding:12px; margin:12px 0; border-radius:6px;">
<b>1️⃣ Clone the Repository</b><br>
<pre>
git clone https://github.com/Lixuan0913/LexiGov.git
cd aseanL-main
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
Create and Add the following inside <code>.env</code>:  
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
http://localhost:10000
</pre>
</div>


</div>
