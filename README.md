# 🔥 நண்பன் AI (Nanban AI)

**Your Tamil Friend - AI Companion that speaks in 5 Tamil dialects with 4 different personalities!**

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)](https://flask.palletsprojects.com/)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o--mini-orange.svg)](https://openai.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 🌟 Features

### 🗣️ 5 Tamil Dialects
- **Chennai (சென்னை)** - Fast, energetic, bold
- **Kovai (கோவை)** - Polite, calm, musical  
- **Madurai (மதுரை)** - Raw, confident, authoritative
- **Nellai (நெல்லை)** - Earthy, rhythmic, lively
- **Eelam (ஈழம்)** - Pure Jaffna Tamil
- **Common (பொதுவான)** - Neutral, universally understood

### 🎭 4 Distinct Personalities
- **Jaliana (ஜாலியான)** - Fun, energetic, uses emojis 😄🔥
- **Amaithiyana (அமைதியான)** - Calm, soft, respectful 😌
- **Thelivana (தெளிவான)** - Direct, logical, no-nonsense 🎯
- **Vilakkamaana (விளக்கமான)** - Teacher-like, detailed explanations 📚

### 🔊 Voice Support
- Text-to-Speech in Tamil
- Different voices for each dialect
- Natural-sounding conversations

### 💭 Smart Features
- **Name Memory** - Remembers and uses your name naturally
- **Conversation History** - Maintains context across messages
- **Cultural Awareness** - Understands Tamil culture and context
- **Emotion Matching** - Adapts to your emotional state

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))
- (Optional) Google Cloud account for better voice

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/nanban-ai.git
cd nanban-ai
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure environment**
```bash
cp .env.example .env
```

Edit `.env` and add your OpenAI API key:
```
OPENAI_API_KEY=sk-your-api-key-here
OPENAI_MODEL=gpt-4o-mini
SECRET_KEY=your-secret-key
DEBUG=True
```

4. **Run the application**
```bash
python app.py
```

5. **Open your browser**
```
http://localhost:5000
```

**That's it! நண்பன் AI is now running! 🎉**

---

## 🏗️ Project Structure

```
nanban-ai/
├── app.py                 # Main Flask application
├── openai_brain.py        # AI logic with Tamil personality system
├── voice_handler.py       # Google Cloud TTS integration
├── database.py            # SQLite database handler
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── templates/            # HTML templates
│   ├── home.html         # Landing page
│   ├── setup.html        # Configuration page
│   └── chat.html         # Chat interface
├── static/              # CSS and JS files
│   └── css/
│       └── style.css     # Global styles
└── README.md            # This file
```

---

## 🌐 Deployment

### Deploy to Railway (Free Tier)

1. Go to [Railway](https://railway.app)
2. Connect your GitHub repository
3. Add environment variables:
   - `OPENAI_API_KEY`
   - `SECRET_KEY`
   - `PORT=5000`
4. Deploy!

### Deploy to Render

1. Go to [Render](https://render.com)
2. Create new Web Service
3. Connect GitHub repository
4. Settings:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
5. Add environment variables
6. Deploy!

### Deploy to Heroku

```bash
heroku create nanban-ai
heroku config:set OPENAI_API_KEY=your-key
heroku config:set SECRET_KEY=your-secret
git push heroku main
```

---

## 💰 Cost Estimate

### OpenAI API (GPT-4o-mini)
- **Per conversation (20 messages):** ~₹0.50-1
- **1,000 conversations/day:** ₹15,000-30,000/month
- **Free tier testing:** $10 credit = ~20,000 messages

### Hosting
- **Railway/Render:** Free tier available
- **Paid tier:** ~₹500-2,000/month

---

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | Your OpenAI API key | ✅ Yes |
| `OPENAI_MODEL` | Model to use (default: gpt-4o-mini) | ❌ No |
| `SECRET_KEY` | Flask secret key | ✅ Yes |
| `DEBUG` | Debug mode (True/False) | ❌ No |
| `PORT` | Port to run on (default: 5000) | ❌ No |
| `GOOGLE_APPLICATION_CREDENTIALS` | Path to Google Cloud JSON key | ❌ No |

---

## 🐛 Troubleshooting

### Common Issues

**"OPENAI_API_KEY not found"**
- Check `.env` file exists
- Ensure no spaces around `=`
- Verify key starts with `sk-`

**"No module named 'openai'"**
```bash
pip install -r requirements.txt
```

**"Insufficient quota"**
- Add credits to OpenAI account
- Minimum $5 required

**Voice not working**
- Voice requires Google Cloud setup (optional)
- Chat works without voice

For more help, see [SETUP_GUIDE.md](SETUP_GUIDE.md)

---

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details.

### Ways to Contribute
- 🐛 Report bugs
- 💡 Suggest features
- 📝 Improve documentation
- 🔧 Submit pull requests
- 🌍 Add more dialects
- 🎨 Improve UI/UX

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

Built with:
- [OpenAI GPT-4o-mini](https://openai.com/) - AI intelligence
- [Google Cloud Text-to-Speech](https://cloud.google.com/text-to-speech) - Tamil voice
- [Flask](https://flask.palletsprojects.com/) - Web framework
- [SQLite](https://www.sqlite.org/) - Database

Special thanks to the Tamil community for inspiration and feedback! 🙏

---

## 🗺️ Roadmap

### Version 1.0 (Current)
- ✅ 5 Tamil dialects
- ✅ 4 personality types
- ✅ Voice support
- ✅ Name memory
- ✅ Web interface

### Version 1.1 (Planned)
- 🔄 Mobile app (React Native)
- 🔄 Voice input (Speech-to-Text)
- 🔄 More dialects
- 🔄 Custom voice cloning
- 🔄 API access

### Version 2.0 (Future)
- 🔮 Multi-language support
- 🔮 Premium features
- 🔮 Business API
- 🔮 Analytics dashboard

---

**Made with ❤️ for the Tamil community**

**"இது AI இல்ல… நம்ம ஊரு நண்பன்!"**
