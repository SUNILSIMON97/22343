# 🔥 NANBAN AI - COMPLETE SETUP GUIDE FOR MACHI 🔥

**Hey Machi! Here's your step-by-step guide to get Nanban AI running by Feb 14!**

---

## 📅 TODAY (Jan 31) - SETUP & FIRST RUN

### STEP 1: Get Your OpenAI API Key (15 minutes)

1. **Go to:** https://platform.openai.com
2. **Click:** "Sign up" (or login if you have account)
3. **After login:**
   - Click your profile (top right)
   - Click "API keys"
   - Click "Create new secret key"
   - **COPY THE KEY!** (looks like: sk-proj-abc123...)
   - **IMPORTANT:** Save it somewhere safe! You can't see it again!

4. **Add credits:**
   - Go to "Billing" section
   - Click "Add payment method"
   - Add ₹850 (about $10 USD)
   - This gives you ~20,000 conversations for testing!

### STEP 2: Install Python (if you don't have it)

**Check if you have Python:**
```bash
python --version
```

**If you see "Python 3.8" or higher → SKIP TO STEP 3**

**If not installed:**

**Windows:**
1. Go to: https://www.python.org/downloads/
2. Download Python 3.11
3. **IMPORTANT:** Check "Add Python to PATH" during installation!
4. Install

**Mac:**
```bash
brew install python3
```

**Linux:**
```bash
sudo apt update
sudo apt install python3 python3-pip
```

### STEP 3: Download Nanban AI Files

You have two options:

**Option A: I'll give you ZIP file**
- Download all files I created
- Extract to folder: `C:\nanban-ai` (Windows) or `~/nanban-ai` (Mac/Linux)

**Option B: If you have the files already**
- Make sure all files are in one folder
- Folder structure should match the README

### STEP 4: Setup Environment

**Open Terminal/Command Prompt:**

**Windows:**
- Press `Win + R`
- Type: `cmd`
- Press Enter

**Mac/Linux:**
- Open Terminal app

**Navigate to project folder:**
```bash
cd C:\nanban-ai          # Windows
cd ~/nanban-ai           # Mac/Linux
```

**Create virtual environment (recommended):**
```bash
python -m venv venv
```

**Activate it:**
```bash
# Windows:
venv\Scripts\activate

# Mac/Linux:
source venv/bin/activate
```

You'll see `(venv)` appear before your command prompt.

**Install dependencies:**
```bash
pip install -r requirements.txt
```

This will take 2-3 minutes. Don't worry about warnings.

### STEP 5: Configure Environment Variables

**Create .env file:**

**Windows:**
```bash
copy .env.example .env
notepad .env
```

**Mac/Linux:**
```bash
cp .env.example .env
nano .env
```

**Edit the file and add your OpenAI key:**
```
OPENAI_API_KEY=sk-your-actual-key-here-from-step-1
OPENAI_MODEL=gpt-4o-mini
SECRET_KEY=nanban-super-secret-key-12345
DEBUG=True
PORT=5000
```

**Save and close** (Ctrl+S, Ctrl+X in nano)

### STEP 6: RUN NANBAN AI! 🚀

```bash
python app.py
```

**You should see:**
```
🔥 NANBAN AI STARTING... 🔥

நண்பன் AI is now running!

🌐 Open your browser and go to:
http://localhost:5000

Press CTRL+C to stop the server.
```

**Open your browser:**
- Type: `http://localhost:5000`
- Press Enter

**YOU SHOULD SEE NANBAN AI HOME PAGE!** 🎉

---

## ✅ FIRST TEST

1. Click "ஆரம்பிக்கலாம்"
2. Enter your name
3. Select slang (try Chennai first)
4. Select persona (try Jaliana)
5. Click "சரி, பேசலாம் வா!"
6. **TYPE:** "Hello nanban!"
7. **WAIT:** AI should respond in Chennai slang!

**IF IT WORKS → YOU'RE DONE! CONGRATS! 🔥**

**IF IT DOESN'T WORK → Check troubleshooting below**

---

## 🚨 TROUBLESHOOTING

### Error: "OPENAI_API_KEY not found"
**Solution:**
- Check your `.env` file exists
- Make sure there's no space around the `=`
- Should be: `OPENAI_API_KEY=sk-abc123` (NO SPACES!)

### Error: "No module named 'openai'"
**Solution:**
```bash
pip install openai
```

### Error: "API key invalid"
**Solution:**
- Check you copied the full key from OpenAI
- Make sure it starts with `sk-`
- Try creating a new key on OpenAI platform

### Error: "Insufficient quota"
**Solution:**
- You need to add credits to OpenAI account
- Go to platform.openai.com → Billing
- Add at least $5 (₹420)

### Browser shows error
**Solution:**
- Check terminal for error messages
- Press `Ctrl+C` to stop server
- Run `python app.py` again
- Refresh browser

### Voice not working
**This is OK for now!**
- Voice needs Google Cloud setup (optional)
- Chat will still work perfectly
- We can add voice later

---

## 📱 NEXT STEPS (Feb 1-13)

### Feb 1-2: Test Everything
- Test all 5 slangs
- Test all 4 personas
- Try different conversations
- Note any bugs

### Feb 3-4: Get Feedback
- Share with 5 friends
- Ask them to test
- Collect feedback
- Fix bugs

### Feb 5-9: Polish
- Improve responses
- Fix any issues
- Make UI prettier
- Add features if needed

### Feb 10-13: Prepare Presentation
- Create demo script
- Practice presentation
- Prepare backup plan
- Test on different devices

### Feb 14: LAUNCH! 🚀
- Present Nanban AI
- Demo live
- Collect feedback
- CELEBRATE! 🎉

---

## 🌐 DEPLOYING ONLINE (After local testing works)

### Option 1: Railway (FREE, EASIEST)

1. **Go to:** https://railway.app
2. **Sign up** with GitHub
3. **Click:** "New Project"
4. **Click:** "Deploy from GitHub repo"
5. **Select:** Your nanban-ai folder
6. **Add Environment Variables:**
   - Click "Variables"
   - Add: `OPENAI_API_KEY` = your key
   - Add: `SECRET_KEY` = random string
   - Add: `PORT` = 5000
7. **Deploy!**

Railway will give you a URL like: `https://nanban-ai-production.up.railway.app`

**SHARE THIS URL WITH ANYONE!**

### Option 2: Render (Also FREE)

1. **Go to:** https://render.com
2. **Sign up** with GitHub
3. **Click:** "New" → "Web Service"
4. **Connect:** GitHub repository
5. **Settings:**
   - Build: `pip install -r requirements.txt`
   - Start: `gunicorn app:app`
6. **Add Environment Variables**
7. **Deploy!**

---

## 💰 COSTS BREAKDOWN

### Development (Now - Feb 14):
- **OpenAI credits:** ₹850 ($10) - enough for 20,000+ test messages
- **Domain (optional):** ₹800/year
- **Total:** ~₹1,650

### After Launch (Monthly):
- **Hosting:** ₹0 (Railway/Render free tier)
- **OpenAI:** ₹500-2,000 (depends on usage)
- **Domain:** ₹70/month (₹800/year)
- **Total:** ₹570-2,070/month

**With 50 premium users (₹199/month):**
- Revenue: ₹9,950/month
- Profit: ₹7,880-9,380/month ✅

---

## 📞 NEED HELP?

**If you get stuck:**

1. **Check error message** in terminal
2. **Google the error** (seriously!)
3. **Check README.md** in project folder
4. **Restart everything:**
   ```bash
   Ctrl+C (stop server)
   python app.py (restart)
   ```

**Common fixes solve 90% of issues:**
- Restart server
- Check .env file
- Reinstall dependencies: `pip install -r requirements.txt`

---

## 🎯 SUCCESS CHECKLIST

Before Feb 14, make sure:

- [ ] Local version running perfectly
- [ ] All 5 slangs working
- [ ] All 4 personas working
- [ ] Tested with 5+ people
- [ ] Deployed online (Railway/Render)
- [ ] Domain connected (optional)
- [ ] Demo prepared
- [ ] Backup video ready
- [ ] Presentation slides done

---

## 🔥 YOU GOT THIS, MACHI!

**Remember:**
- Don't aim for perfection
- Done > Perfect
- Launch and iterate
- Get feedback and improve

**15 days is enough!**

You have:
- ✅ Solid idea
- ✅ Complete code (I built it!)
- ✅ Clear plan
- ✅ Budget (₹50K)

**Just execute step by step.**

**Nanban AI will be LIVE by Feb 14! 🚀🔥**

**Let's gooooo!** 💪

---

**Any questions? Any errors? Tell me and I'll fix it!**

**Your virtual partner,**
**Machi (Claude) 🤝**
