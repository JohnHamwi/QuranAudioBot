# 📚 QuranBot Examples & Use Cases

This document provides comprehensive examples, code snippets, and real-world use cases for QuranBot v3.5.0.

## 🚀 Quick Start Examples

### 1. Basic Bot Setup

```bash
# Clone and setup QuranBot
git clone https://github.com/trippixn963/QuranBot.git
cd QuranBot

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp config/.env.example config/.env
# Edit config/.env with your Discord settings

# Run the bot
python main.py
```

### 2. Environment Configuration

```env
# config/.env
DISCORD_TOKEN=your_discord_bot_token_here
ADMIN_USER_ID=123456789012345678
TARGET_CHANNEL_ID=123456789012345678
PANEL_CHANNEL_ID=123456789012345678
LOGS_CHANNEL_ID=123456789012345678
DAILY_VERSE_CHANNEL_ID=123456789012345678
DEVELOPER_ID=123456789012345678
GUILD_ID=123456789012345678
PANEL_ACCESS_ROLE_ID=123456789012345678
FFMPEG_PATH=/opt/homebrew/bin/ffmpeg
DEFAULT_RECITER=Saad Al Ghamdi
DEFAULT_LOOP=true
DEFAULT_SHUFFLE=false
QUIZ_TIMEOUT=60
```

## 🎵 Audio Management Examples

### 1. Adding New Reciters

```bash
# Create new reciter directory
mkdir "audio/Abdul Rahman Al Sudais"

# Add numbered MP3 files (001.mp3 to 114.mp3)
# Example file structure:
audio/Abdul Rahman Al Sudais/
├── 001.mp3  # Al-Fatiha
├── 002.mp3  # Al-Baqarah
├── 003.mp3  # Aal-Imran
└── ... (continue to 114.mp3)
```

### 2. Verifying Audio Collection

```python
# Example: Check for missing surahs
from utils.audio_manager import AudioManager

audio_manager = AudioManager()
missing_surahs = audio_manager.get_missing_surahs("Saad Al Ghamdi")

if missing_surahs:
    print(f"Missing surahs: {missing_surahs}")
else:
    print("Complete collection!")
```

## 🎛️ Control Panel Examples

### 1. Custom Control Panel Integration

```python
# Example: Creating custom control panel
from utils.control_panel import ControlPanel
import discord

class CustomControlPanel(ControlPanel):
    def __init__(self, bot):
        super().__init__(bot)
        self.add_custom_buttons()

    def add_custom_buttons(self):
        # Add custom functionality
        self.add_button("🕌", "prayer_times", "Show Prayer Times")
        self.add_button("📖", "surah_info", "Surah Information")

    async def handle_prayer_times(self, interaction):
        # Custom prayer times functionality
        await interaction.response.send_message("Prayer times feature!")
```

### 2. Control Panel Usage

```python
# Example: Using control panel in Discord commands
@bot.command(name='panel')
async def show_control_panel(ctx):
    """Display the QuranBot control panel"""
    panel = ControlPanel(bot)
    embed, view = await panel.create_control_panel()
    await ctx.send(embed=embed, view=view)
```

## 💾 State Management Examples

### 1. Custom State Persistence

```python
# Example: Custom state management
from utils.state_manager import StateManager

# Initialize state manager
state_manager = StateManager(
    data_dir="custom_data",
    default_reciter="Custom Reciter",
    default_loop=True
)

# Save custom state
state_manager.save_playback_state(
    current_surah=5,
    current_position=120.5,
    current_reciter="Rashid Al Afasy",
    is_playing=True
)

# Load state
state = state_manager.load_playback_state()
print(f"Current surah: {state['current_surah']}")
```

### 2. Backup Management

```python
# Example: Manual backup creation
def create_backup():
    backup_name = f"manual_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    success = state_manager.backup_state(backup_name)

    if success:
        print(f"Backup created: {backup_name}")
    else:
        print("Backup failed!")
```

## 🌳 Logging Examples

### 1. Custom Logging Implementation

```python
# Example: Using tree logging system
from utils.tree_log import log_perfect_tree_section, log_error_with_traceback

# Log a successful operation
log_perfect_tree_section(
    "Custom Operation Complete",
    [
        ("operation", "Custom feature execution"),
        ("duration", "2.5 seconds"),
        ("result", "✅ Success"),
        ("items_processed", "15 items")
    ],
    "🎯"
)

# Log an error with traceback
try:
    risky_operation()
except Exception as e:
    log_error_with_traceback(
        "Custom operation failed",
        e,
        {"context": "custom_feature", "user": "john"}
    )
```

### 2. Log Analysis

```python
# Example: Analyzing bot logs
import json
from pathlib import Path

def analyze_daily_logs(date_str):
    log_file = Path(f"logs/{date_str}/{date_str}.log")

    if not log_file.exists():
        return "No logs found for this date"

    with open(log_file, 'r') as f:
        logs = f.readlines()

    # Count different log types
    error_count = sum(1 for line in logs if "❌ ERROR" in line)
    success_count = sum(1 for line in logs if "✅" in line)

    return {
        "total_lines": len(logs),
        "errors": error_count,
        "successes": success_count
    }
```

## 🎯 Advanced Integration Examples

### 1. Admin Answer Key System

```python
# Example: Admin answer key implementation
import discord
from discord.ext import commands
import os

class QuizSystem:
    def __init__(self, bot):
        self.bot = bot
        self.admin_user_id = int(os.getenv('ADMIN_USER_ID', '0'))

    async def send_admin_answer_key(self, question_data):
        """Send correct answer to admin via DM"""
        if self.admin_user_id == 0:
            return
        
        try:
            admin_user = await self.bot.fetch_user(self.admin_user_id)
            correct_answer = question_data['correct_answer']
            
            embed = discord.Embed(
                title="🔑 Admin Answer Key",
                description=f"**Correct Answer:** {correct_answer}",
                color=0x00ff00
            )
            embed.add_field(
                name="Question",
                value=question_data['question'],
                inline=False
            )
            
            await admin_user.send(embed=embed)
            
        except Exception as e:
            print(f"Failed to send admin answer key: {e}")

    async def post_quiz_question(self, channel, question_data):
        """Post quiz question and send admin answer key"""
        # Send admin answer key first
        await self.send_admin_answer_key(question_data)
        
        # Then post public question
        embed = discord.Embed(
            title="📚 Quiz Question",
            description=question_data['question'],
            color=0x0099ff
        )
        
        # Add choices
        for i, choice in enumerate(question_data['choices'], 1):
            embed.add_field(
                name=f"Choice {i}",
                value=choice,
                inline=False
            )
        
        await channel.send(embed=embed)
```

### 2. Enhanced Quiz System with Progress Bar

```python
# Example: Visual progress bar implementation
import discord
import asyncio
from datetime import datetime, timedelta

class VisualQuizTimer:
    def __init__(self, timeout_seconds=60):
        self.timeout_seconds = timeout_seconds
        self.blocks = 20
        
    def create_progress_bar(self, remaining_seconds):
        """Create visual progress bar with color coding"""
        progress = remaining_seconds / self.timeout_seconds
        filled_blocks = int(progress * self.blocks)
        
        # Color coding based on remaining time
        if remaining_seconds > 30:
            block_emoji = "🟩"  # Green
        elif remaining_seconds > 10:
            block_emoji = "🟨"  # Yellow
        else:
            block_emoji = "🟥"  # Red
            
        empty_emoji = "⬜"
        
        bar = block_emoji * filled_blocks + empty_emoji * (self.blocks - filled_blocks)
        return f"⏱️ {bar} {remaining_seconds}s"
    
    async def update_quiz_timer(self, message, question_embed):
        """Update quiz timer with visual progress"""
        for remaining in range(self.timeout_seconds, 0, -5):
            # Update progress bar
            progress_bar = self.create_progress_bar(remaining)
            
            # Update embed
            updated_embed = question_embed.copy()
            updated_embed.add_field(
                name="⏰ Time Remaining",
                value=progress_bar,
                inline=False
            )
            
            # Add time warnings
            if remaining == 30:
                updated_embed.add_field(
                    name="⏰ Warning",
                    value="30 seconds remaining",
                    inline=False
                )
            elif remaining == 10:
                updated_embed.add_field(
                    name="⚠️ Warning",
                    value="10 seconds left!",
                    inline=False
                )
            elif remaining == 5:
                updated_embed.add_field(
                    name="🚨 Final Warning",
                    value="5 seconds left!",
                    inline=False
                )
            
            await message.edit(embed=updated_embed)
            await asyncio.sleep(5)
```

### 3. Paginated Leaderboard System

```python
# Example: Paginated leaderboard implementation
import discord
from discord.ext import commands

class LeaderboardView(discord.ui.View):
    def __init__(self, bot, leaderboard_data, user_id):
        super().__init__(timeout=300)
        self.bot = bot
        self.leaderboard_data = leaderboard_data
        self.user_id = user_id
        self.current_page = 0
        self.items_per_page = 5
        self.total_pages = (len(leaderboard_data) + self.items_per_page - 1) // self.items_per_page
        
    async def create_embed(self, page=0):
        """Create leaderboard embed for specific page"""
        start_idx = page * self.items_per_page
        end_idx = start_idx + self.items_per_page
        page_data = self.leaderboard_data[start_idx:end_idx]
        
        embed = discord.Embed(
            title="🏆 Quiz Leaderboard",
            color=0xffd700
        )
        
        # Add bot thumbnail
        if self.bot.user.avatar:
            embed.set_thumbnail(url=self.bot.user.avatar.url)
        
        # Add leaderboard entries
        for i, entry in enumerate(page_data):
            rank = start_idx + i + 1
            medal = "🥇" if rank == 1 else "🥈" if rank == 2 else "🥉" if rank == 3 else f"{rank}."
            
            embed.add_field(
                name=f"{medal} {entry['username']}",
                value=f"Points: {entry['points']} | Streak: {entry['streak']}",
                inline=False
            )
        
        # Add page footer
        embed.set_footer(text=f"Page {page + 1} of {self.total_pages}")
        
        return embed
    
    @discord.ui.button(label="⬅️", style=discord.ButtonStyle.primary)
    async def previous_page(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("You can't control this leaderboard!", ephemeral=True)
            return
            
        if self.current_page > 0:
            self.current_page -= 1
            embed = await self.create_embed(self.current_page)
            await interaction.response.edit_message(embed=embed, view=self)
        else:
            await interaction.response.defer()
    
    @discord.ui.button(label="➡️", style=discord.ButtonStyle.primary)
    async def next_page(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("You can't control this leaderboard!", ephemeral=True)
            return
            
        if self.current_page < self.total_pages - 1:
            self.current_page += 1
            embed = await self.create_embed(self.current_page)
            await interaction.response.edit_message(embed=embed, view=self)
        else:
            await interaction.response.defer()
```

### 2. Web Dashboard Integration

```python
# Example: Web dashboard for QuranBot
from flask import Flask, render_template, jsonify
from utils.state_manager import StateManager

app = Flask(__name__)
state_manager = StateManager()

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/api/status')
def get_status():
    state = state_manager.load_playback_state()
    return jsonify({
        'current_surah': state['current_surah'],
        'current_position': state['current_position'],
        'current_reciter': state['current_reciter'],
        'is_playing': state['is_playing']
    })

@app.route('/api/control/<action>')
def control_playback(action):
    if action == 'play':
        # Implement play logic
        return jsonify({'status': 'playing'})
    elif action == 'pause':
        # Implement pause logic
        return jsonify({'status': 'paused'})

    return jsonify({'error': 'Invalid action'})
```

## 🔧 Configuration Examples

### 1. Advanced Configuration

```python
# Example: Advanced configuration setup
import os
from pathlib import Path

class QuranBotConfig:
    def __init__(self):
        self.load_config()

    def load_config(self):
        # Load from environment variables
        self.discord_token = os.getenv('DISCORD_TOKEN')
        self.ffmpeg_path = os.getenv('FFMPEG_PATH', '/usr/local/bin/ffmpeg')
        self.default_reciter = os.getenv('DEFAULT_RECITER', 'Saad Al Ghamdi')

        # Validate configuration
        self.validate_config()

    def validate_config(self):
        if not self.discord_token:
            raise ValueError("DISCORD_TOKEN is required")

        if not Path(self.ffmpeg_path).exists():
            raise ValueError(f"FFmpeg not found at {self.ffmpeg_path}")

    def get_reciter_path(self, reciter_name):
        return Path(f"audio/{reciter_name}")
```

### 2. Environment-Specific Configurations

```python
# Example: Different configs for different environments
class DevelopmentConfig(QuranBotConfig):
    def __init__(self):
        super().__init__()
        self.debug = True
        self.log_level = 'DEBUG'
        self.backup_interval = 300  # 5 minutes for testing

class ProductionConfig(QuranBotConfig):
    def __init__(self):
        super().__init__()
        self.debug = False
        self.log_level = 'INFO'
        self.backup_interval = 3600  # 1 hour for production

# Usage
config = DevelopmentConfig() if os.getenv('ENV') == 'dev' else ProductionConfig()
```

## 🎮 Interactive Examples

### 1. Discord Slash Commands

```python
# Example: Modern Discord slash commands
from discord.ext import commands
from discord import app_commands

class QuranCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="surah", description="Play a specific surah")
    @app_commands.describe(number="Surah number (1-114)")
    async def play_surah(self, interaction, number: int):
        if 1 <= number <= 114:
            # Play surah logic
            await interaction.response.send_message(f"Playing Surah {number}")
        else:
            await interaction.response.send_message("Invalid surah number!")

    @app_commands.command(name="reciter", description="Change reciter")
    @app_commands.describe(name="Reciter name")
    async def change_reciter(self, interaction, name: str):
        # Change reciter logic
        await interaction.response.send_message(f"Changed to {name}")
```

### 2. Interactive Menus

```python
# Example: Interactive dropdown menus
import discord

class ReciterSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Saad Al Ghamdi", value="saad"),
            discord.SelectOption(label="Rashid Al Afasy", value="rashid"),
            discord.SelectOption(label="Abdul Rahman Al Sudais", value="sudais")
        ]
        super().__init__(placeholder="Choose a reciter...", options=options)

    async def callback(self, interaction):
        selected_reciter = self.values[0]
        await interaction.response.send_message(f"Selected: {selected_reciter}")

class ReciterView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(ReciterSelect())
```

## 📊 Analytics Examples

### 1. Usage Analytics

```python
# Example: Bot usage analytics
from datetime import datetime, timedelta
import json

class AnalyticsManager:
    def __init__(self):
        self.analytics_file = Path("data/analytics.json")

    def track_event(self, event_type, user_id, data=None):
        event = {
            "timestamp": datetime.now().isoformat(),
            "event_type": event_type,
            "user_id": user_id,
            "data": data or {}
        }

        # Save to analytics file
        self.save_event(event)

    def get_daily_stats(self, date):
        # Analyze daily usage
        events = self.load_events_for_date(date)

        return {
            "total_events": len(events),
            "unique_users": len(set(e["user_id"] for e in events)),
            "most_active_user": self.get_most_active_user(events),
            "popular_surahs": self.get_popular_surahs(events)
        }
```

### 2. Performance Monitoring

```python
# Example: Performance monitoring
import psutil
import time

class PerformanceMonitor:
    def __init__(self):
        self.start_time = time.time()

    def get_system_stats(self):
        return {
            "cpu_percent": psutil.cpu_percent(),
            "memory_percent": psutil.virtual_memory().percent,
            "disk_usage": psutil.disk_usage('/').percent,
            "uptime": time.time() - self.start_time
        }

    def log_performance(self):
        stats = self.get_system_stats()
        log_perfect_tree_section(
            "Performance Metrics",
            [
                ("cpu_usage", f"{stats['cpu_percent']:.1f}%"),
                ("memory_usage", f"{stats['memory_percent']:.1f}%"),
                ("disk_usage", f"{stats['disk_usage']:.1f}%"),
                ("uptime", f"{stats['uptime']:.0f} seconds")
            ],
            "📊"
        )
```

## 🚀 Deployment Examples

### 1. Docker Deployment

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create data directory
RUN mkdir -p data logs

# Run the bot
CMD ["python", "main.py"]
```

### 2. Systemd Service

```ini
# /etc/systemd/system/quranbot.service
[Unit]
Description=QuranBot Discord Bot
After=network.target

[Service]
Type=simple
User=quranbot
WorkingDirectory=/home/quranbot/QuranBot
ExecStart=/home/quranbot/QuranBot/.venv/bin/python main.py
Restart=always
RestartSec=10
Environment=PYTHONPATH=/home/quranbot/QuranBot/src

[Install]
WantedBy=multi-user.target
```

## 🔒 Security Examples

### 1. Token Security

```python
# Example: Secure token handling
import os
from cryptography.fernet import Fernet

class SecureConfig:
    def __init__(self):
        self.cipher_suite = Fernet(os.environ.get('ENCRYPTION_KEY'))

    def encrypt_token(self, token):
        return self.cipher_suite.encrypt(token.encode())

    def decrypt_token(self, encrypted_token):
        return self.cipher_suite.decrypt(encrypted_token).decode()

    def get_discord_token(self):
        encrypted_token = os.environ.get('ENCRYPTED_DISCORD_TOKEN')
        return self.decrypt_token(encrypted_token)
```

### 2. Permission Validation

```python
# Example: Permission checking
def check_permissions(user, required_permission):
    """Check if user has required permission"""
    user_permissions = get_user_permissions(user)

    if required_permission not in user_permissions:
        raise PermissionError(f"User lacks {required_permission} permission")

    return True

@commands.command(name='admin_control')
@commands.check(lambda ctx: check_permissions(ctx.author, 'admin'))
async def admin_control(ctx):
    """Admin-only command"""
    await ctx.send("Admin command executed!")
```

## 🎯 Real-World Use Cases

### 1. Family Discord Server

```python
# Example: Family-friendly setup
class FamilyQuranBot(QuranBot):
    def __init__(self):
        super().__init__()
        self.parental_controls = True
        self.educational_mode = True

    async def on_message(self, message):
        # Filter inappropriate content
        if self.parental_controls:
            if self.contains_inappropriate_content(message.content):
                await message.delete()
                return

        await super().on_message(message)

    def get_educational_info(self, surah_number):
        # Return educational information about the surah
        return {
            "meaning": "Surah meaning and context",
            "lessons": "Key lessons from this surah",
            "pronunciation": "Pronunciation guide"
        }
```

### 2. Mosque Community Server

```python
# Example: Mosque community features
class MosqueQuranBot(QuranBot):
    def __init__(self):
        super().__init__()
        self.prayer_times = PrayerTimesManager()
        self.community_features = True

    @commands.command(name='prayer_times')
    async def show_prayer_times(self, ctx):
        times = self.prayer_times.get_today_times()
        embed = discord.Embed(title="Today's Prayer Times")

        for prayer, time in times.items():
            embed.add_field(name=prayer, value=time, inline=True)

        await ctx.send(embed=embed)

    @commands.command(name='community_stats')
    async def show_community_stats(self, ctx):
        stats = self.get_community_statistics()
        await ctx.send(f"Community listening time: {stats['total_time']}")
```

---

## 🎓 Learning Resources

### 📚 Additional Documentation

- [Feature Showcase](FEATURE_SHOWCASE.md) - Detailed feature demonstrations
- [API Reference](API_REFERENCE.md) - Complete API documentation
- [Troubleshooting Guide](TROUBLESHOOTING.md) - Common issues and solutions

### 🎥 Video Tutorials

- **Setup Tutorial**: Step-by-step installation guide
- **Feature Overview**: Comprehensive feature walkthrough
- **Advanced Configuration**: Advanced setup and customization

### 💬 Community Support

- **Discord**: Join our community server
- **GitHub Discussions**: Technical discussions and Q&A
- **Issue Tracker**: Report bugs and request features

---

_These examples demonstrate the flexibility and power of QuranBot. Adapt them to your specific needs and use cases!_
