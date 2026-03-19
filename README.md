## ⚙️ Setup Guide

Follow these steps to run the ASEAN Multilingual AI Assistant locally.

---

### 🧊 Quick Setup (All-in-One) ###


> **1️⃣ Clone the Repository**
```bash  
git clone https://github.com/your-username/your-repo.git  
cd LexiGov

> **2️⃣ Install Dependencies**
```bash    
pip install -r requirements.txt  

> **3️⃣ Create .env file**
```bash  
(add the following inside .env)  
GOOGLE_API_KEY=your_google_api_key  
HF_TOKEN=your_huggingface_token  
GOOGLE_APPLICATION_CREDENTIALS=./credentials.json  

> **4️⃣ Run the Server**
```bash   
python app.py 

> **5️⃣ Open in Browser**
```bash  
http://localhost:5000  

