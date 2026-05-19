# Streamlit Deployment Guide 🚀

## Local Testing

Before deploying, test your Streamlit app locally:

```bash
cd C:\Users\RC\Desktop\chatbot
pip install streamlit
streamlit run streamlit_app.py
```

Open http://localhost:8501 in your browser.

---

## Option 1: Streamlit Cloud (EASIEST & FREE ⭐)

### Step 1: Prepare Your GitHub Repository

1. Create a GitHub account (if you don't have one): https://github.com/signup
2. Create a new repository named `chatbot` (or any name)
3. Push your files to GitHub:

```bash
cd C:\Users\RC\Desktop\chatbot

# Initialize git (if not already done)
git init
git add .
git commit -m "Initial commit: AeroFuel Chatbot"

# Add remote and push (replace with your GitHub repo URL)
git remote add origin https://github.com/YOUR_USERNAME/chatbot.git
git branch -M main
git push -u origin main
```

### Step 2: Deploy to Streamlit Cloud

1. Go to https://share.streamlit.io
2. Sign up with your GitHub account
3. Click **"New app"**
4. Select:
   - **Repository**: your-username/chatbot
   - **Branch**: main
   - **Main file path**: streamlit_app.py
5. Click **"Deploy!"**

✅ Your app will be live in 1-2 minutes at: `https://your-username-chatbot.streamlit.app`

---

## Option 2: Heroku (Paid, but simple)

1. Go to https://heroku.com and create account
2. Install Heroku CLI
3. Create `Procfile` in your project folder:
```
web: streamlit run streamlit_app.py
```
4. Deploy:
```bash
heroku login
heroku create your-chatbot-name
git push heroku main
```

---

## Option 3: Railway.app (Paid alternative)

1. Go to https://railway.app
2. Connect your GitHub repo
3. Deploy automatically

---

## Recommended Setup

**Best option for beginners**: Streamlit Cloud
- Free tier available
- Auto-deploys from GitHub (push → live)
- No credit card required
- Perfect for hobby projects

---

## After Deployment

Once deployed, you can:
- Share your link with anyone
- See live analytics in Streamlit Cloud dashboard
- Redeploy by pushing to GitHub (automatic)
