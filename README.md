# 🕌 QuranBot - Discord Quran Audio Bot

A professional Discord bot that streams Quran recitations with interactive features, quizzes, and comprehensive VPS deployment tools.

![QuranBot Banner](images/BANNER%20(Still).png)

## ✨ Features

### 🎵 Audio Streaming
- **High-quality Quran recitations** from multiple renowned reciters
- **Continuous playback** with seamless transitions between surahs
- **Voice channel integration** with automatic connection management
- **Audio controls** (play, pause, skip, volume control)

### 📖 Interactive Commands
- **Daily verses** with automatic scheduling and beautiful embeds
- **Quran quizzes** with multiple choice questions and leaderboards
- **Verse lookup** with translation and recitation
- **Listening statistics** and user engagement tracking

### 🏆 Gamification
- **Quiz leaderboards** with scoring and rankings
- **Listening time tracking** and user statistics
- **Interactive challenges** and knowledge testing
- **Progress tracking** across sessions

### 🛠️ Professional Infrastructure
- **Production-ready VPS deployment** with automated scripts
- **Real-time web dashboard** for monitoring and control
- **Comprehensive logging** with structured output
- **Backup systems** with automatic data protection
- **State persistence** across restarts and crashes

### 🌐 VPS Management
- **One-command deployment** to any VPS
- **Web dashboard** accessible via browser
- **Nginx configuration** for custom domains
- **Systemd services** for 24/7 operation
- **Log syncing** between VPS and local machine

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Discord Bot Token ([Get one here](https://discord.com/developers/applications))
- VPS (optional, for 24/7 hosting)

### Local Development

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/QuranBot.git
cd QuranBot
```

2. **Set up virtual environment**
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

3. **Configure environment**
```bash
cp config/.env.example config/.env
# Edit config/.env with your Discord bot token
```

4. **Run the bot**
```bash
python main.py
```

### VPS Deployment

For 24/7 hosting, deploy to your VPS:

1. **Configure VPS settings**
```bash
export VPS_IP="your.vps.ip.address"
export VPS_USER="root"
```

2. **Deploy to VPS**
```bash
cd vps/deployment
./deploy-to-discordbots.sh
```

3. **Access web dashboard**
```
http://your.vps.ip.address:8080
```

See [VPS_CONFIG_TEMPLATE.md](vps/VPS_CONFIG_TEMPLATE.md) for detailed configuration.

## 📋 Commands

| Command | Description | Usage |
|---------|-------------|-------|
| `/verse` | Get a specific Quran verse | `/verse 2:255` |
| `/daily-verse` | Get today's daily verse | `/daily-verse` |
| `/question` | Start a Quran quiz | `/question` |
| `/leaderboard` | View quiz rankings | `/leaderboard` |
| `/interval` | Set daily verse timing | `/interval 6:00` |
| `/credits` | Bot information | `/credits` |

## 🏗️ Architecture

### Project Structure
```
QuranBot/
├── src/                    # Core bot source code
│   ├── bot/               # Main bot initialization
│   ├── commands/          # Discord slash commands
│   └── utils/             # Utility modules
├── vps/                   # VPS deployment tools
│   ├── deployment/        # Deployment scripts
│   ├── web_dashboard/     # Real-time monitoring
│   ├── nginx/             # Web server configuration
│   ├── scripts/           # Management utilities
│   └── systemd/           # Service configurations
├── config/                # Configuration files
├── tests/                 # Unit tests
├── audio/                 # Quran audio files
├── images/                # Bot assets
└── tools/                 # Development utilities
```

### Key Components

- **Bot Core** (`src/bot/main.py`) - Main Discord bot logic
- **Audio Manager** (`src/utils/audio_manager.py`) - Handles audio streaming
- **Quiz System** (`src/utils/quiz_manager.py`) - Interactive quiz functionality
- **State Management** (`src/utils/state_manager.py`) - Persistent data storage
- **Web Dashboard** (`vps/web_dashboard/app.py`) - Real-time monitoring interface

## 🖥️ Web Dashboard

The included web dashboard provides:

- **Real-time bot monitoring** - Status, uptime, resource usage
- **System metrics** - CPU, memory, disk usage with progress bars
- **Log viewing** - Live log streaming and error tracking
- **Bot controls** - Start, stop, restart functionality
- **Statistics** - Usage analytics and performance metrics

Access at: `http://your-vps-ip:8080`

## 🔧 Configuration

### Environment Variables

Create `config/.env` with:

```bash
# Discord Configuration
DISCORD_TOKEN=your_bot_token_here
GUILD_ID=your_guild_id_here

# Audio Configuration  
FFMPEG_PATH=/usr/bin/ffmpeg  # Linux: /usr/bin/ffmpeg, macOS: /opt/homebrew/bin/ffmpeg

# Optional: Bot Customization
BOT_NAME=QuranBot
BOT_VERSION=1.0.0
```

### Audio Files

Place Quran audio files in the `audio/` directory:
```
audio/
├── Reciter Name/
│   ├── 001.mp3  # Al-Fatihah
│   ├── 002.mp3  # Al-Baqarah
│   └── ...
```

## 🧪 Testing

Run the test suite:
```bash
python -m pytest tests/
```

Individual test modules:
```bash
python -m pytest tests/test_audio_manager.py
python -m pytest tests/test_quiz_manager.py
```

## 📊 Monitoring & Logging

### Structured Logging
- **Daily log files** in `logs/YYYY-MM-DD/`
- **Error tracking** with full stack traces
- **Performance metrics** and usage statistics
- **Tree-style output** for easy reading

### Web Dashboard
- **Real-time monitoring** of bot status
- **System resource tracking** 
- **Live log streaming**
- **Interactive controls**

### VPS Log Syncing
```bash
# Sync logs from VPS to local machine
cd vps/scripts
./sync_logs.sh
```

## 🚀 Deployment Options

### Option 1: Local Development
- Run locally for testing and development
- Suitable for small servers or testing

### Option 2: VPS Deployment
- 24/7 hosting with automatic restarts
- Web dashboard for monitoring
- Production-ready with systemd services

### Option 3: Cloud Hosting
- Deploy to any cloud provider
- Scalable and reliable
- Use provided deployment scripts

## 🛡️ Security

- **Environment variables** for sensitive data
- **Comprehensive .gitignore** prevents credential leaks
- **Input validation** on all user commands
- **Error handling** prevents crashes and data exposure
- **Backup encryption** for data protection

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Quran audio** from various renowned reciters
- **Discord.py** library for Discord integration
- **FFmpeg** for audio processing
- **Flask** for the web dashboard
- **Community contributors** and testers

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/QuranBot/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/QuranBot/discussions)
- **Documentation**: See `/docs` folder for detailed guides

## 🔄 Version History

- **v1.0.0** - Initial release with core features
- **v1.1.0** - Added VPS deployment system
- **v1.2.0** - Web dashboard and monitoring
- **v1.3.0** - Enhanced quiz system and leaderboards

---

**Made with ❤️ for the Muslim community** 