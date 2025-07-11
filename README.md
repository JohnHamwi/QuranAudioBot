# 🕌 QuranBot - Discord Quran Audio Bot

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Discord.py](https://img.shields.io/badge/Discord.py-2.3+-5865F2.svg?style=for-the-badge&logo=discord&logoColor=white)](https://discordpy.readthedocs.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](LICENSE)
[![Version](https://img.shields.io/badge/Version-v3.5.0-orange.svg?style=for-the-badge)](https://github.com/trippixn963/QuranBot/releases)

*"And We have certainly made the Qur'an easy for remembrance, so is there any who will remember?"* - **Quran 54:17**

A professional Discord bot designed to bring the beauty of Quranic recitation to Muslim communities worldwide. Stream high-quality Quran audio, engage with interactive Islamic knowledge quizzes, and strengthen your connection to the Holy Quran through technology.

**بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيم**  
*In the name of Allah, the Most Gracious, the Most Merciful*

![QuranBot Banner](images/BANNER%20(Still).png)

## 🌟 Islamic Features

### 📿 Quranic Audio Experience
- **Beautiful recitations** from renowned Qaris including Saad Al Ghamdi, Abdul Rahman Al-Sudais, and more
- **Continuous Tilawah** with seamless transitions between Surahs
- **Voice channel integration** for community listening experiences
- **Multiple reciter support** to experience different Qira'at styles

### 📖 Islamic Knowledge & Learning
- **Daily Ayah delivery** with automatic scheduling for consistent Islamic reminders
- **Quranic knowledge quizzes** to test understanding of Islamic teachings
- **Verse lookup system** with translations for deeper comprehension
- **Interactive learning** designed to strengthen Islamic knowledge

### 🏆 Community Engagement
- **Leaderboards** for Islamic quiz competitions
- **Listening statistics** to track your Quranic engagement
- **Community challenges** to encourage collective Islamic learning
- **Progress tracking** for personal spiritual development

### 🛠️ Professional Islamic Bot Infrastructure
- **Comprehensive logging** with Islamic date support
- **Backup systems** protecting your Islamic community data
- **State persistence** ensuring uninterrupted service
- **Error handling** for reliable Islamic content delivery

## 🚀 Quick Start - Serving the Ummah

### Prerequisites
- Python 3.9+ 
- Discord Bot Token ([Create one here](https://discord.com/developers/applications))
- FFmpeg for audio processing

### Local Development

1. **Clone the repository**
```bash
git clone https://github.com/trippixn963/QuranBot.git
cd QuranBot
```

2. **Set up virtual environment**
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

3. **Configure for your Islamic community**
```bash
cp config/.env.example config/.env
# Edit config/.env with your Discord bot token and server settings
```

4. **Begin serving your community**
```bash
python main.py
```

## 📋 Islamic Commands

| Command | Islamic Purpose | Usage |
|---------|----------------|-------|
| `/verse` | Retrieve specific Quranic verses | `/verse 2:255` (Ayat al-Kursi) |
| `/question` | Test Islamic knowledge | `/question` |
| `/leaderboard` | View community Islamic quiz rankings | `/leaderboard` |
| `/interval` | Schedule daily Islamic reminders | `/interval 6:00` |
| `/credits` | Bot and Islamic acknowledgments | `/credits` |

## 🏗️ Architecture - Built for the Ummah

### Project Structure
```
QuranBot/
├── src/                    # Core Islamic bot functionality
│   ├── bot/               # Main bot initialization
│   ├── commands/          # Islamic Discord commands
│   └── utils/             # Islamic utility modules
├── config/                # Islamic community configuration
├── tests/                 # Quality assurance tests
├── docs/                  # Documentation
├── audio/                 # Quranic recitation files
├── images/                # Islamic bot assets
└── tools/                 # Islamic development utilities
```

### Key Islamic Components

- **Bot Core** (`src/bot/main.py`) - Main Islamic Discord bot logic
- **Audio Manager** (`src/utils/audio_manager.py`) - Quranic audio streaming
- **Quiz System** (`src/utils/quiz_manager.py`) - Islamic knowledge testing
- **State Management** (`src/utils/state_manager.py`) - Islamic data persistence
- **Rich Presence** (`src/utils/rich_presence.py`) - Discord status integration

## 🔧 Islamic Community Configuration

### Environment Variables

Configure for your Islamic community in `config/.env`:

```bash
# Discord Configuration for Islamic Community
DISCORD_TOKEN=your_bot_token_here
GUILD_ID=your_islamic_server_id_here

# Quranic Audio Configuration  
FFMPEG_PATH=/usr/bin/ffmpeg  # Linux: /usr/bin/ffmpeg, macOS: /opt/homebrew/bin/ffmpeg

# Islamic Bot Customization
BOT_NAME=QuranBot
BOT_VERSION=3.5.0
```

### Quranic Audio Files

Organize your Quranic recitations in the `audio/` directory:
```
audio/
├── Saad Al Ghamdi/
│   ├── 001.mp3  # Al-Fatihah
│   ├── 002.mp3  # Al-Baqarah
│   └── ...
├── Abdul Rahman Al-Sudais/
│   ├── 001.mp3  # Al-Fatihah
│   └── ...
```

## 🧪 Quality Assurance - Serving Excellence

Run the comprehensive test suite:
```bash
python -m pytest tests/
```

Test individual Islamic components:
```bash
python -m pytest tests/test_audio_manager.py  # Quranic audio tests
python -m pytest tests/test_quiz_manager.py   # Islamic knowledge tests
python -m pytest tests/test_integration.py    # Discord integration tests
```

## 📊 Islamic Community Monitoring & Logging

### Structured Islamic Logging
- **Daily log files** with Islamic date tracking in `logs/YYYY-MM-DD/`
- **Error tracking** ensuring reliable Islamic service
- **Islamic engagement metrics** and community statistics
- **Beautiful tree-style output** for easy Islamic bot monitoring

### Log Management
- **Automatic log rotation** preventing disk space issues
- **Structured JSON logging** for easy analysis
- **Real-time error tracking** with Discord notifications
- **Performance monitoring** ensuring smooth Islamic content delivery

## 🚀 Deployment Options for Islamic Communities

### Option 1: Local Islamic Community
- Run locally for small Islamic communities or testing
- Perfect for local mosque or Islamic center Discord servers
- Easy setup and configuration

### Option 2: Cloud Islamic Service
- Deploy to any cloud provider serving the global Ummah
- Scalable Islamic bot infrastructure
- Use Docker for containerized deployment

### Option 3: Self-Hosted Islamic Service
- Host on your own server for complete control
- Perfect for larger Islamic communities
- Customize as needed for your specific requirements

## 🛡️ Security - Protecting Islamic Communities

- **Environment variables** protecting sensitive Islamic community data
- **Comprehensive .gitignore** preventing credential exposure
- **Input validation** on all Islamic commands
- **Error handling** ensuring stable Islamic service
- **Backup encryption** protecting Islamic community data

## 🤝 Contributing to the Islamic Community

Join our efforts to serve the Ummah:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/islamic-enhancement`)
3. Commit your changes (`git commit -m 'Add Islamic feature for community benefit'`)
4. Push to the branch (`git push origin feature/islamic-enhancement`)
5. Open a Pull Request to benefit the global Muslim community

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Islamic Acknowledgments

**"And whoever does a good deed, We will increase for him good therein. Indeed, Allah is Forgiving and Appreciative."** - *Quran 42:23*

- **Quranic recitations** from renowned Qaris serving the Ummah
- **Discord.py** library enabling Islamic community connections
- **FFmpeg** for processing beautiful Quranic audio
- **Muslim developers and contributors** strengthening the global Islamic community

## 📞 Islamic Community Support

- **Issues**: [GitHub Issues](https://github.com/trippixn963/QuranBot/issues) for technical Islamic bot support
- **Discussions**: [GitHub Discussions](https://github.com/trippixn963/QuranBot/discussions) for Islamic community discussions
- **Documentation**: [API Reference](docs/API_REFERENCE.md) for comprehensive command documentation

## 🔄 Version History - Serving the Ummah

- **v1.0.0** - Initial release serving Islamic communities
- **v1.1.0** - Enhanced audio system for better Quranic experience
- **v1.2.0** - Islamic community quiz system and leaderboards
- **v1.3.0** - Advanced state management and logging
- **v3.5.0** - Professional Islamic bot infrastructure with comprehensive testing

## 📍 Community Attribution

Originally created for **discord.gg/syria** - Building bridges within the global Islamic community.

> **📚 Educational Purpose**  
> This project is provided "AS-IS" for educational purposes, designed to help Muslim communities learn and implement Islamic Discord bot technology. No official support, help, or maintenance is offered. Use with the intention of benefiting the Ummah and at your own discretion.

---

[![GitHub Stars](https://img.shields.io/github/stars/trippixn963/QuranBot?style=social)](https://github.com/trippixn963/QuranBot/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/trippixn963/QuranBot?style=social)](https://github.com/trippixn963/QuranBot/network/members)
[![Discord Server](https://img.shields.io/badge/Discord-syria-7289DA?style=flat-square&logo=discord&logoColor=white)](https://discord.gg/syria)
[![Open Source](https://img.shields.io/badge/Open%20Source-%E2%9D%A4-ff69b4?style=flat-square)](https://opensource.org/)

**Made with ❤️ for the Muslim community**

---

### 🤲 A Note from the Creator

*"And whoever does a good deed, We will increase for him good therein. Indeed, Allah is Forgiving and Appreciative."* - **Quran 42:23*

This Islamic community project was created with love and respect for the Muslim Ummah by a Christian developer who believes in the beauty of interfaith collaboration and the power of technology to serve religious communities. May this tool benefit Muslim communities worldwide in their spiritual journey and strengthen bonds within the global Ummah.

**Created with respect and admiration for the Islamic faith** 🤝 