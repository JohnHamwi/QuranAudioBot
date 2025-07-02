import discord
from discord import app_commands
from discord.ui import View, Button, Select
import time
import os
import asyncio
import traceback
import logging
from typing import Optional, Dict, Any
from datetime import datetime

# Use the main logger from utils
from utils.logger import logger

def log_operation(operation: str, level: str = "INFO", extra: Optional[Dict[str, Any]] = None, error: Optional[Exception] = None):
    """Enhanced logging with operation tracking and structured data."""
    emoji_map = {
        "init": "🚀", "auth": "🔐", "button": "🔘", "embed": "📋", 
        "channel": "📺", "voice": "🎵", "error": "❌", "success": "✅",
        "check": "🔍", "panel": "🎛️", "user": "👤", "guild": "🏠",
        "reciter": "🎤", "surah": "📖", "next": "⏭️", "prev": "⏮️", "credits": "📋",
        "loop": "🔁", "shuffle": "🔀"
    }
    
    emoji = emoji_map.get(operation, "ℹ️")
    level_emoji = {"DEBUG": "🔍", "INFO": "ℹ️", "WARNING": "⚠️", "ERROR": "❌", "CRITICAL": "🔥"}
    
    # Format timestamp with new format: MM-DD | HH:MM:SS AM/PM
    timestamp = datetime.now().strftime('%m-%d | %I:%M:%S %p')
    
    log_data = {
        "operation": operation,
        "timestamp": timestamp,
        "component": "control_panel"
    }
    
    if extra:
        log_data.update(extra)
    
    if error:
        log_data["error"] = str(error)
        log_data["error_type"] = type(error).__name__
        log_data["traceback"] = traceback.format_exc()
        level = "ERROR"
    
    # Include user information in the main log message if available
    user_info = ""
    if extra and "user_name" in extra and "user_id" in extra:
        user_info = f" | 👤 {extra['user_name']} ({extra['user_id']})"
    
    log_message = f"{emoji} {level_emoji.get(level, 'ℹ️')} Control Panel - {operation.upper()}{user_info}"
    
    if level == "DEBUG":
        logger.debug(log_message, extra={"extra": log_data})
    elif level == "INFO":
        logger.info(log_message, extra={"extra": log_data})
    elif level == "WARNING":
        logger.warning(log_message, extra={"extra": log_data})
    elif level == "ERROR":
        logger.error(log_message, extra={"extra": log_data})
    elif level == "CRITICAL":
        logger.critical(log_message, extra={"extra": log_data})

def is_in_voice_channel(interaction: discord.Interaction) -> bool:
    """Check if the user is in the voice channel with enhanced logging."""
    try:
        log_operation("check", "DEBUG", {
            "user_id": interaction.user.id,
            "user_name": interaction.user.name,
            "guild_id": interaction.guild.id if interaction.guild else None,
            "channel_id": interaction.channel.id if interaction.channel else None,
            "check_type": "voice_channel"
        })
        
        from utils.config import Config
        target_channel_id = Config.TARGET_CHANNEL_ID
        
        # Check if user has voice state (Member objects have voice state)
        if not isinstance(interaction.user, discord.Member):
            log_operation("check", "WARNING", {
                "user_id": interaction.user.id,
                "user_name": interaction.user.name,
                "reason": "user_not_member",
                "check_type": "voice_channel"
            })
            return False
        
        member = interaction.user
        if not member.voice or not member.voice.channel:
            log_operation("check", "WARNING", {
                "user_id": member.id,
                "user_name": member.name,
                "reason": "user_not_in_voice",
                "check_type": "voice_channel"
            })
            return False
        
        if member.voice.channel.id == target_channel_id:
            log_operation("check", "INFO", {
                "user_id": member.id,
                "user_name": member.name,
                "voice_channel_id": member.voice.channel.id,
                "voice_channel_name": member.voice.channel.name,
                "check_type": "voice_channel",
                "result": "success"
            })
            return True
        
        log_operation("check", "WARNING", {
            "user_id": member.id,
            "user_name": member.name,
            "user_voice_channel_id": member.voice.channel.id,
            "user_voice_channel_name": member.voice.channel.name,
            "target_channel_id": target_channel_id,
            "check_type": "voice_channel",
            "result": "wrong_channel"
        })
        return False
        
    except Exception as e:
        log_operation("check", "ERROR", {
            "user_id": interaction.user.id if interaction.user else None,
            "check_type": "voice_channel",
            "error_details": "voice_channel_check_failed"
        }, e)
        return False

class SurahSelect(Select):
    def __init__(self, bot, page=0):
        from utils.surah_mapper import get_surah_display_name
        current_reciter = getattr(bot, 'current_reciter', None)
        audio_files = bot.get_audio_files() if current_reciter else []
        
        # Get all available surahs
        all_surahs = []
        seen = set()
        for file in audio_files:
            name = os.path.basename(file)
            if name.endswith('.mp3'):
                surah_num = name.split('.')[0]
                if surah_num not in seen:
                    seen.add(surah_num)
                    try:
                        surah_num_int = int(surah_num)
                        surah_name = get_surah_display_name(surah_num_int)
                        all_surahs.append((surah_num_int, surah_num, surah_name))
                    except Exception:
                        continue
        
        # Sort by surah number
        all_surahs.sort(key=lambda x: x[0])
        
        # Calculate pagination
        items_per_page = 25
        total_pages = (len(all_surahs) + items_per_page - 1) // items_per_page
        start_idx = page * items_per_page
        end_idx = min(start_idx + items_per_page, len(all_surahs))
        
        # Create options for current page
        surah_options = []
        for surah_num_int, surah_num, surah_name in all_surahs[start_idx:end_idx]:
            surah_options.append(discord.SelectOption(
                label=f"{surah_num.zfill(3)} - {surah_name}", 
                value=surah_num,
                description=f"Surah {surah_num_int}"
            ))
        
        # Create placeholder with page info
        placeholder = f"Select Surah... (Page {page + 1}/{total_pages})"
        
        super().__init__(placeholder=placeholder, min_values=1, max_values=1, options=surah_options, custom_id=f"select_surah_page_{page}")
        self.bot = bot
        self.page = page
        self.total_pages = total_pages
        self.all_surahs = all_surahs
    async def callback(self, interaction: discord.Interaction):
        # Intensive logging for surah selection
        log_operation("surah", "INFO", {
            "user_id": interaction.user.id,
            "user_name": interaction.user.name,
            "user_display_name": interaction.user.display_name,
            "guild_id": interaction.guild.id if interaction.guild else None,
            "guild_name": interaction.guild.name if interaction.guild else None,
            "channel_id": interaction.channel.id if interaction.channel else None,
            "channel_name": getattr(interaction.channel, 'name', 'DM') if interaction.channel else None,
            "action": "surah_selection_started",
            "selected_surah": self.values[0],
            "timestamp": datetime.now().isoformat()
        })
        
        if not is_in_voice_channel(interaction):
            log_operation("surah", "WARNING", {
                "user_id": interaction.user.id,
                "user_name": interaction.user.name,
                "action": "surah_selection_denied",
                "reason": "not_in_voice_channel",
                "selected_surah": self.values[0]
            })
            await interaction.response.send_message("❌ You must be in the voice channel to use this!", ephemeral=True)
            return
        
        surah_num = self.values[0]
        
        # Respond immediately to prevent timeout
        await interaction.response.send_message(f"✅ Jumping to Surah {surah_num}...", ephemeral=True)
        
        # Get current state before change
        old_index = self.bot.state_manager.get_current_song_index()
        old_song = self.bot.state_manager.get_current_song_name()
        
        # Set new surah index
        self.bot.state_manager.set_current_song_index_by_surah(surah_num, self.bot.get_audio_files())
        new_index = self.bot.state_manager.get_current_song_index()
        
        # Do the heavy work in the background
        async def restart_playback():
            try:
                # Stop current playback and restart
                self.bot.is_streaming = False
                await asyncio.sleep(2)  # Wait for current playback to stop
                
                # Get the voice client and restart playback
                voice_client = None
                for guild in self.bot.guilds:
                    if guild.voice_client:
                        voice_client = guild.voice_client
                        break
                
                if voice_client and voice_client.is_connected():
                    # Restart playback with new surah
                    self.bot.is_streaming = True
                    # Start a new playback task
                    asyncio.create_task(self.bot.play_quran_files(voice_client, voice_client.channel))
                    
                    log_operation("surah", "INFO", {
                        "user_id": interaction.user.id,
                        "user_name": interaction.user.name,
                        "action": "surah_selection_successful",
                        "selected_surah": surah_num,
                        "old_index": old_index,
                        "new_index": new_index,
                        "old_song": old_song,
                        "voice_client_connected": True,
                        "playback_restarted": True
                    })
                else:
                    log_operation("surah", "ERROR", {
                        "user_id": interaction.user.id,
                        "user_name": interaction.user.name,
                        "action": "surah_selection_failed",
                        "selected_surah": surah_num,
                        "reason": "voice_client_not_available",
                        "voice_client_found": voice_client is not None,
                        "voice_client_connected": voice_client.is_connected() if voice_client else False
                    })
            except Exception as e:
                log_operation("surah", "ERROR", {
                    "user_id": interaction.user.id,
                    "user_name": interaction.user.name,
                    "action": "surah_selection_background_failed",
                    "selected_surah": surah_num,
                    "error": str(e)
                }, e)
        
        # Start the background task
        asyncio.create_task(restart_playback())

class ReciterSelect(Select):
    def __init__(self, bot):
        from utils.config import Config
        reciters = bot.get_available_reciters()
        current_reciter = getattr(bot, 'current_reciter', None)
        options = [discord.SelectOption(label=r, value=r, default=(r==current_reciter)) for r in reciters]
        super().__init__(placeholder="Select Reciter...", min_values=1, max_values=1, options=options, custom_id="select_reciter")
        self.bot = bot
    async def callback(self, interaction: discord.Interaction):
        # Intensive logging for reciter selection
        channel_name = getattr(interaction.channel, 'name', 'DM') if interaction.channel else None
            
        log_operation("reciter", "INFO", {
            "user_id": interaction.user.id,
            "user_name": interaction.user.name,
            "user_display_name": interaction.user.display_name,
            "guild_id": interaction.guild.id if interaction.guild else None,
            "guild_name": interaction.guild.name if interaction.guild else None,
            "channel_id": interaction.channel.id if interaction.channel else None,
            "channel_name": channel_name,
            "action": "reciter_selection_started",
            "selected_reciter": self.values[0],
            "current_reciter": getattr(self.bot, 'current_reciter', 'Unknown'),
            "timestamp": datetime.now().isoformat()
        })
        
        if not is_in_voice_channel(interaction):
            log_operation("reciter", "WARNING", {
                "user_id": interaction.user.id,
                "user_name": interaction.user.name,
                "action": "reciter_selection_denied",
                "reason": "not_in_voice_channel",
                "selected_reciter": self.values[0]
            })
            await interaction.response.send_message("❌ You must be in the voice channel to use this!", ephemeral=True)
            return
        
        reciter = self.values[0]
        current_index = self.bot.state_manager.get_current_song_index()
        current_song = self.bot.state_manager.get_current_song_name()
        surah_num = None
        if current_song:
            try:
                surah_num = current_song.split('.')[0]
            except Exception:
                pass
        
        # Switch reciter
        success = self.bot.set_current_reciter(reciter)
        if not success:
            log_operation("reciter", "ERROR", {
                "user_id": interaction.user.id,
                "user_name": interaction.user.name,
                "action": "reciter_switch_failed",
                "selected_reciter": reciter,
                "reason": "reciter_not_found"
            })
            await interaction.response.send_message(f"❌ Failed to switch to reciter: {reciter}", ephemeral=True)
            return
        
        # Respond immediately to prevent timeout
        await interaction.response.send_message(f"✅ Switching to reciter: {reciter}...", ephemeral=True)
        
        # Get new audio files for the new reciter
        files = self.bot.get_audio_files()
        jump_index = 0
        if surah_num:
            for i, f in enumerate(files):
                if os.path.basename(f).startswith(surah_num):
                    jump_index = i
                    break
        
        # Update state and restart playback
        self.bot.state_manager.set_current_song_index(jump_index)
        
        # Do the heavy work in the background
        async def restart_playback():
            try:
                # Stop current playback and restart
                self.bot.is_streaming = False
                await asyncio.sleep(2)  # Wait for current playback to stop
                
                # Get the voice client and restart playback
                voice_client = None
                for guild in self.bot.guilds:
                    if guild.voice_client:
                        voice_client = guild.voice_client
                        break
                
                if voice_client and voice_client.is_connected():
                    # Restart playback with new reciter
                    self.bot.is_streaming = True
                    # Start a new playback task
                    asyncio.create_task(self.bot.play_quran_files(voice_client, voice_client.channel))
                    
                    log_operation("reciter", "INFO", {
                        "user_id": interaction.user.id,
                        "user_name": interaction.user.name,
                        "action": "reciter_switch_successful",
                        "selected_reciter": reciter,
                        "surah_num": surah_num,
                        "old_index": current_index,
                        "new_index": jump_index,
                        "old_song": current_song,
                        "voice_client_connected": True,
                        "playback_restarted": True
                    })
                else:
                    log_operation("reciter", "ERROR", {
                        "user_id": interaction.user.id,
                        "user_name": interaction.user.name,
                        "action": "reciter_switch_failed",
                        "selected_reciter": reciter,
                        "reason": "voice_client_not_available",
                        "voice_client_found": voice_client is not None,
                        "voice_client_connected": voice_client.is_connected() if voice_client else False
                    })
            except Exception as e:
                log_operation("reciter", "ERROR", {
                    "user_id": interaction.user.id,
                    "user_name": interaction.user.name,
                    "action": "reciter_switch_background_failed",
                    "selected_reciter": reciter,
                    "error": str(e)
                }, e)
        
        # Start the background task
        asyncio.create_task(restart_playback())
        log_operation("reciter", "INFO", {"user_id": interaction.user.id, "reciter": reciter, "surah_num": surah_num, "action": "select_reciter"})

class ControlPanelView(View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot
        self.current_surah_page = 0
        self.surah_select = SurahSelect(bot, self.current_surah_page)
        self.add_item(self.surah_select)
        self.add_item(ReciterSelect(bot))
    
    def update_surah_select(self):
        """Update the surah select dropdown with current page"""
        # Remove old surah select
        for item in self.children[:]:
            if isinstance(item, SurahSelect):
                self.remove_item(item)
                break
        
        # Create new surah select for current page
        self.surah_select = SurahSelect(self.bot, self.current_surah_page)
        
        # Find the position of the reciter select to insert surah select before it
        reciter_index = None
        for i, item in enumerate(self.children):
            if isinstance(item, ReciterSelect):
                reciter_index = i
                break
        
        # Insert surah select at the beginning (before reciter)
        if reciter_index is not None:
            self.children.insert(0, self.surah_select)
        else:
            self.add_item(self.surah_select)
    
    # Row 1: Surah & Reciter Selection (Main Controls)
    # Row 2: Page Navigation
    @discord.ui.button(label="◀️ Previous Page", style=discord.ButtonStyle.secondary, custom_id="surah_prev_page", row=2)
    async def surah_prev_page(self, interaction: discord.Interaction, button: Button):
        if not is_in_voice_channel(interaction):
            await interaction.response.send_message("❌ You must be in the voice channel to use this!", ephemeral=True)
            return
        
        if self.current_surah_page > 0:
            self.current_surah_page -= 1
            
            # Create a new view with the updated page
            new_view = ControlPanelView(self.bot)
            new_view.current_surah_page = self.current_surah_page
            
            # Update the surah select to the new page
            for item in new_view.children[:]:
                if isinstance(item, SurahSelect):
                    new_view.remove_item(item)
                    break
            new_view.add_item(SurahSelect(self.bot, self.current_surah_page))
            
            # Update the message with new view
            embed = interaction.message.embeds[0] if interaction.message and interaction.message.embeds else None
            await interaction.response.edit_message(embed=embed, view=new_view)
            
            log_operation("page", "INFO", {
                "user_id": interaction.user.id,
                "user_name": interaction.user.name,
                "action": "surah_prev_page",
                "new_page": self.current_surah_page + 1,
                "total_pages": SurahSelect(self.bot, self.current_surah_page).total_pages
            })
        else:
            await interaction.response.send_message("⚠️ Already on the first page.", ephemeral=True)
    
    @discord.ui.button(label="Next Page ▶️", style=discord.ButtonStyle.secondary, custom_id="surah_next_page", row=2)
    async def surah_next_page(self, interaction: discord.Interaction, button: Button):
        if not is_in_voice_channel(interaction):
            await interaction.response.send_message("❌ You must be in the voice channel to use this!", ephemeral=True)
            return
        
        if self.current_surah_page < self.surah_select.total_pages - 1:
            self.current_surah_page += 1
            
            # Create a new view with the updated page
            new_view = ControlPanelView(self.bot)
            new_view.current_surah_page = self.current_surah_page
            
            # Update the surah select to the new page
            for item in new_view.children[:]:
                if isinstance(item, SurahSelect):
                    new_view.remove_item(item)
                    break
            new_view.add_item(SurahSelect(self.bot, self.current_surah_page))
            
            # Update the message with new view
            embed = interaction.message.embeds[0] if interaction.message and interaction.message.embeds else None
            await interaction.response.edit_message(embed=embed, view=new_view)
            
            log_operation("page", "INFO", {
                "user_id": interaction.user.id,
                "user_name": interaction.user.name,
                "action": "surah_next_page", 
                "new_page": self.current_surah_page + 1,
                "total_pages": SurahSelect(self.bot, self.current_surah_page).total_pages
            })
        else:
            await interaction.response.send_message("⚠️ Already on the last page.", ephemeral=True)
    
    @discord.ui.button(label="📋 Credits", style=discord.ButtonStyle.primary, custom_id="credits", row=2)
    async def credits_button(self, interaction: discord.Interaction, button: Button):
        # Intensive logging for credits button
        channel_name = getattr(interaction.channel, 'name', 'DM') if interaction.channel else None
        
        log_operation("credits", "INFO", {
            "user_id": interaction.user.id,
            "user_name": interaction.user.name,
            "user_display_name": interaction.user.display_name,
            "guild_id": interaction.guild.id if interaction.guild else None,
            "guild_name": interaction.guild.name if interaction.guild else None,
            "channel_id": interaction.channel.id if interaction.channel else None,
            "channel_name": channel_name,
            "action": "credits_button_clicked",
            "timestamp": datetime.now().isoformat()
        })
        
        # Get available reciters
        bot = interaction.client
        reciters = getattr(bot, 'get_available_reciters', lambda: [])()
        reciters_text = "\n".join([f"• {reciter}" for reciter in reciters])
        
        # Create credits embed (exact same as /credits command)
        embed = discord.Embed(
            title="🕌 QuranBot Credits & Information",
            description="A 24/7 Quran streaming bot with multiple reciters and interactive controls.",
            color=discord.Color.blue()
        )
        
        # Bot Information
        embed.add_field(
            name="🤖 Bot Information",
            value=f"**Name:** Syrian Quran\n"
                  f"**Version:** 2.0.0\n"
                  f"**Status:** 24/7 Streaming\n"
                  f"**Current Reciter:** {getattr(interaction.client, 'current_reciter', 'Unknown')}\n"
                  f"**Total Surahs:** 114",
            inline=False
        )
        
        # Creator Information
        embed.add_field(
            name="👨‍💻 Creator",
            value="**Developer:** <@259725211664908288>\n"
                  "**Role:** Full-Stack Developer & Bot Creator\n"
                  "**GitHub:** [QuranBot Repository](https://github.com/JohnHamwi/QuranAudioBot)",
            inline=False
        )
        
        # Available Reciters
        embed.add_field(
            name=f"🎤 Available Reciters ({len(reciters)})",
            value=reciters_text if reciters else "No reciters available",
            inline=False
        )
        
        # Technologies Used
        embed.add_field(
            name="🛠️ Technologies Used",
            value="**Core Framework:** Discord.py\n"
                  "**Audio Processing:** FFmpeg\n"
                  "**Language:** Python 3.13\n"
                  "**Database:** SQLite (State Management)\n"
                  "**Logging:** Enhanced Structured Logging\n"
                  "**Architecture:** Service-Oriented Design",
            inline=False
        )
        
        # Features
        embed.add_field(
            name="✨ Features",
            value="• 24/7 Continuous Quran Streaming\n"
                  "• Multiple Reciter Support\n"
                  "• Interactive Control Panel\n"
                  "• Dynamic Rich Presence",
            inline=False
        )
        
        # Beta Testing Warning
        embed.add_field(
            name="⚠️ Beta Testing Notice",
            value="**This bot is currently in beta testing.**\n\n"
                  "If you encounter any bugs or issues, please DM <@259725211664908288> to report them.\n\n"
                  "Your feedback helps improve the bot!",
            inline=False
        )
        
        embed.set_footer(text="Made with ❤️ for the Muslim Ummah • QuranBot v2.0.0")
        embed.timestamp = discord.utils.utcnow()
        
        # Set creator's Discord profile picture
        try:
            creator_user = await interaction.client.fetch_user(259725211664908288)
            if creator_user and creator_user.avatar:
                embed.set_thumbnail(url=creator_user.avatar.url)
        except Exception as e:
            log_operation("credits", "WARNING", {
                "user_id": interaction.user.id,
                "user_name": interaction.user.name,
                "action": "creator_avatar_fetch_failed",
                "error": str(e)
            })
            # Fallback to guild icon if creator avatar fails
            try:
                if interaction.guild and interaction.guild.icon:
                    embed.set_thumbnail(url=interaction.guild.icon.url)
            except:
                pass
        
        await interaction.response.send_message(embed=embed, ephemeral=True)
        
        log_operation("credits", "INFO", {
            "user_id": interaction.user.id,
            "user_name": interaction.user.name,
            "action": "credits_displayed",
            "reciters_count": len(reciters),
            "current_reciter": getattr(interaction.client, 'current_reciter', 'Unknown')
        })
    
    # Row 3: Playback Controls
    @discord.ui.button(label="⏮️ Previous", style=discord.ButtonStyle.danger, custom_id="previous", row=3)
    async def previous_button(self, interaction: discord.Interaction, button: Button):
        # Intensive logging for previous button
        channel_name = getattr(interaction.channel, 'name', 'DM') if interaction.channel else None
        
        log_operation("prev", "INFO", {
            "user_id": interaction.user.id,
            "user_name": interaction.user.name,
            "user_display_name": interaction.user.display_name,
            "guild_id": interaction.guild.id if interaction.guild else None,
            "guild_name": interaction.guild.name if interaction.guild else None,
            "channel_id": interaction.channel.id if interaction.channel else None,
            "channel_name": channel_name,
            "action": "previous_button_clicked",
            "timestamp": datetime.now().isoformat()
        })
        
        if not is_in_voice_channel(interaction):
            log_operation("prev", "WARNING", {
                "user_id": interaction.user.id,
                "user_name": interaction.user.name,
                "action": "previous_button_denied",
                "reason": "not_in_voice_channel"
            })
            await interaction.response.send_message("❌ You must be in the voice channel to use this!", ephemeral=True)
            return
        
        idx = self.bot.state_manager.get_current_song_index()
        if idx > 0:
            # Respond immediately to prevent timeout
            await interaction.response.send_message("⏮️ Switching to previous surah...", ephemeral=True)
            
            # Get current state before change
            old_index = idx
            old_song = self.bot.state_manager.get_current_song_name()
            
            # Set new index
            self.bot.state_manager.set_current_song_index(idx-1)
            new_index = idx-1
            
            # Do the heavy work in the background
            async def restart_playback():
                try:
                    # Stop current playback and restart
                    self.bot.is_streaming = False
                    await asyncio.sleep(2)  # Wait for current playback to stop
                    
                    # Get the voice client and restart playback
                    voice_client = None
                    for guild in self.bot.guilds:
                        if guild.voice_client:
                            voice_client = guild.voice_client
                            break
                    
                    if voice_client and voice_client.is_connected():
                        # Restart playback with new surah
                        self.bot.is_streaming = True
                        # Start a new playback task
                        asyncio.create_task(self.bot.play_quran_files(voice_client, voice_client.channel))
                        
                        log_operation("prev", "INFO", {
                            "user_id": interaction.user.id,
                            "user_name": interaction.user.name,
                            "action": "previous_button_successful",
                            "old_index": old_index,
                            "new_index": new_index,
                            "old_song": old_song,
                            "voice_client_connected": True,
                            "playback_restarted": True
                        })
                    else:
                        log_operation("prev", "ERROR", {
                            "user_id": interaction.user.id,
                            "user_name": interaction.user.name,
                            "action": "previous_button_failed",
                            "reason": "voice_client_not_available",
                            "voice_client_found": voice_client is not None,
                            "voice_client_connected": voice_client.is_connected() if voice_client else False
                        })
                except Exception as e:
                    log_operation("prev", "ERROR", {
                        "user_id": interaction.user.id,
                        "user_name": interaction.user.name,
                        "action": "previous_button_background_failed",
                        "error": str(e)
                    }, e)
            
            # Start the background task
            asyncio.create_task(restart_playback())
        else:
            log_operation("prev", "WARNING", {
                "user_id": interaction.user.id,
                "user_name": interaction.user.name,
                "action": "previous_button_denied",
                "reason": "already_at_first_surah",
                "current_index": idx
            })
            await interaction.response.send_message("⚠️ Already at the first surah.", ephemeral=True)
    
    @discord.ui.button(label="🔁 Loop", style=discord.ButtonStyle.secondary, custom_id="loop", row=3)
    async def loop_button(self, interaction: discord.Interaction, button: Button):
        # Intensive logging for loop button
        channel_name = getattr(interaction.channel, 'name', 'DM') if interaction.channel else None
        
        log_operation("loop", "INFO", {
            "user_id": interaction.user.id,
            "user_name": interaction.user.name,
            "user_display_name": interaction.user.display_name,
            "guild_id": interaction.guild.id if interaction.guild else None,
            "guild_name": interaction.guild.name if interaction.guild else None,
            "channel_id": interaction.channel.id if interaction.channel else None,
            "channel_name": channel_name,
            "action": "loop_button_clicked",
            "timestamp": datetime.now().isoformat()
        })
        
        if not is_in_voice_channel(interaction):
            log_operation("loop", "WARNING", {
                "user_id": interaction.user.id,
                "user_name": interaction.user.name,
                "action": "loop_button_denied",
                "reason": "not_in_voice_channel"
            })
            await interaction.response.send_message("❌ You must be in the voice channel to use this!", ephemeral=True)
            return
        
        # Toggle loop mode
        loop_enabled = self.bot.toggle_loop()
        
        # Update button appearance
        if loop_enabled:
            button.style = discord.ButtonStyle.success
            button.label = "🔁 Loop ON"
            status_message = "🔁 Loop mode enabled - Current surah will repeat"
        else:
            button.style = discord.ButtonStyle.secondary
            button.label = "🔁 Loop"
            status_message = "🔁 Loop mode disabled - Normal playback resumed"
        
        log_operation("loop", "INFO", {
            "user_id": interaction.user.id,
            "user_name": interaction.user.name,
            "action": "loop_toggle_successful",
            "loop_enabled": loop_enabled,
            "current_surah": self.bot.current_audio_file
        })
        
        await interaction.response.send_message(status_message, ephemeral=True)
    
    @discord.ui.button(label="🔀 Shuffle", style=discord.ButtonStyle.secondary, custom_id="shuffle", row=3)
    async def shuffle_button(self, interaction: discord.Interaction, button: Button):
        # Intensive logging for shuffle button
        channel_name = getattr(interaction.channel, 'name', 'DM') if interaction.channel else None
        
        log_operation("shuffle", "INFO", {
            "user_id": interaction.user.id,
            "user_name": interaction.user.name,
            "user_display_name": interaction.user.display_name,
            "guild_id": interaction.guild.id if interaction.guild else None,
            "guild_name": interaction.guild.name if interaction.guild else None,
            "channel_id": interaction.channel.id if interaction.channel else None,
            "channel_name": channel_name,
            "action": "shuffle_button_clicked",
            "timestamp": datetime.now().isoformat()
        })
        
        if not is_in_voice_channel(interaction):
            log_operation("shuffle", "WARNING", {
                "user_id": interaction.user.id,
                "user_name": interaction.user.name,
                "action": "shuffle_button_denied",
                "reason": "not_in_voice_channel"
            })
            await interaction.response.send_message("❌ You must be in the voice channel to use this!", ephemeral=True)
            return
        
        # Toggle shuffle mode
        shuffle_enabled = self.bot.toggle_shuffle()
        
        # Update button appearance
        if shuffle_enabled:
            button.style = discord.ButtonStyle.success
            button.label = "🔀 Shuffle ON"
            status_message = "🔀 Shuffle mode enabled - Surahs will play in random order"
        else:
            button.style = discord.ButtonStyle.secondary
            button.label = "🔀 Shuffle"
            status_message = "🔀 Shuffle mode disabled - Normal order resumed"
        
        log_operation("shuffle", "INFO", {
            "user_id": interaction.user.id,
            "user_name": interaction.user.name,
            "action": "shuffle_toggle_successful",
            "shuffle_enabled": shuffle_enabled,
            "total_surahs": len(self.bot.get_audio_files())
        })
        
        await interaction.response.send_message(status_message, ephemeral=True)
    
    @discord.ui.button(label="⏭️ Next", style=discord.ButtonStyle.success, custom_id="skip", row=3)
    async def skip_button(self, interaction: discord.Interaction, button: Button):
        # Intensive logging for next button
        channel_name = getattr(interaction.channel, 'name', 'DM') if interaction.channel else None
        
        log_operation("next", "INFO", {
            "user_id": interaction.user.id,
            "user_name": interaction.user.name,
            "user_display_name": interaction.user.display_name,
            "guild_id": interaction.guild.id if interaction.guild else None,
            "guild_name": interaction.guild.name if interaction.guild else None,
            "channel_id": interaction.channel.id if interaction.channel else None,
            "channel_name": channel_name,
            "action": "next_button_clicked",
            "timestamp": datetime.now().isoformat()
        })
        
        if not is_in_voice_channel(interaction):
            log_operation("next", "WARNING", {
                "user_id": interaction.user.id,
                "user_name": interaction.user.name,
                "action": "next_button_denied",
                "reason": "not_in_voice_channel"
            })
            await interaction.response.send_message("❌ You must be in the voice channel to use this!", ephemeral=True)
            return
        
        files = self.bot.get_audio_files()
        idx = self.bot.state_manager.get_current_song_index()
        if idx < len(files)-1:
            # Respond immediately to prevent timeout
            await interaction.response.send_message("⏭️ Switching to next surah...", ephemeral=True)
            
            # Get current state before change
            old_index = idx
            old_song = self.bot.state_manager.get_current_song_name()
            
            # Set new index
            self.bot.state_manager.set_current_song_index(idx+1)
            new_index = idx+1
            
            # Do the heavy work in the background
            async def restart_playback():
                try:
                    # Stop current playback and restart
                    self.bot.is_streaming = False
                    await asyncio.sleep(2)  # Wait for current playback to stop
                    
                    # Get the voice client and restart playback
                    voice_client = None
                    for guild in self.bot.guilds:
                        if guild.voice_client:
                            voice_client = guild.voice_client
                            break
                    
                    if voice_client and voice_client.is_connected():
                        # Restart playback with new surah
                        self.bot.is_streaming = True
                        # Start a new playback task
                        asyncio.create_task(self.bot.play_quran_files(voice_client, voice_client.channel))
                        
                        log_operation("next", "INFO", {
                            "user_id": interaction.user.id,
                            "user_name": interaction.user.name,
                            "action": "next_button_successful",
                            "old_index": old_index,
                            "new_index": new_index,
                            "old_song": old_song,
                            "voice_client_connected": True,
                            "playback_restarted": True
                        })
                    else:
                        log_operation("next", "ERROR", {
                            "user_id": interaction.user.id,
                            "user_name": interaction.user.name,
                            "action": "next_button_failed",
                            "reason": "voice_client_not_available",
                            "voice_client_found": voice_client is not None,
                            "voice_client_connected": voice_client.is_connected() if voice_client else False
                        })
                except Exception as e:
                    log_operation("next", "ERROR", {
                        "user_id": interaction.user.id,
                        "user_name": interaction.user.name,
                        "action": "next_button_background_failed",
                        "error": str(e)
                    }, e)
            
            # Start the background task
            asyncio.create_task(restart_playback())
        else:
            log_operation("next", "WARNING", {
                "user_id": interaction.user.id,
                "user_name": interaction.user.name,
                "action": "next_button_denied",
                "reason": "already_at_last_surah",
                "current_index": idx,
                "total_files": len(files)
            })
            await interaction.response.send_message("⚠️ Already at the last surah.", ephemeral=True)
    


async def setup(bot):
    """Setup the control panel and create the panel with enhanced logging."""
    try:
        log_operation("init", "INFO", {
            "component": "setup",
            "bot_name": bot.user.name if bot.user else "Unknown"
        })
        
        # Create the control panel in the specified channel
        try:
            from utils.config import Config
            panel_channel_id = Config.PANEL_CHANNEL_ID
        except ImportError as e:
            log_operation("error", "CRITICAL", {
                "component": "setup",
                "error_details": "config_import_failed",
                "error": str(e)
            })
            return
        except AttributeError as e:
            log_operation("error", "CRITICAL", {
                "component": "setup",
                "error_details": "panel_channel_id_not_found",
                "error": str(e)
            })
            return
        
        log_operation("init", "INFO", {
            "component": "setup",
            "panel_channel_id": panel_channel_id
        })
        
        async def create_panel():
            """Create the control panel in the specified text channel with enhanced logging."""
            try:
                log_operation("panel", "INFO", {
                    "component": "create_panel",
                    "panel_channel_id": panel_channel_id
                })
                
                # Find the panel channel directly
                panel_channel = None
                for guild in bot.guilds:
                    try:
                        channel = guild.get_channel(panel_channel_id)
                        if channel:
                            if isinstance(channel, discord.TextChannel):
                                panel_channel = channel
                                log_operation("channel", "INFO", {
                                    "component": "create_panel",
                                    "channel_id": channel.id,
                                    "channel_name": channel.name,
                                    "guild_id": guild.id,
                                    "guild_name": guild.name
                                })
                                break
                    except Exception as e:
                        log_operation("error", "WARNING", {
                            "component": "create_panel",
                            "error_details": "guild_channel_search_failed",
                            "guild_id": guild.id,
                            "error": str(e)
                        })
                        continue
                
                if not panel_channel:
                    log_operation("error", "ERROR", {
                        "component": "create_panel",
                        "panel_channel_id": panel_channel_id,
                        "error_details": "channel_not_found",
                        "available_guilds": [guild.name for guild in bot.guilds]
                    })
                    return
                
                # Check if a control panel already exists and delete it
                try:
                    async for message in panel_channel.history(limit=50):
                        # Check if this message has our control panel embed
                        if (message.embeds and 
                            message.embeds[0].title == "🎵 QuranBot Control Panel" and
                            message.author == bot.user):
                            
                            log_operation("check", "INFO", {
                                "component": "create_panel",
                                "action": "existing_panel_found",
                                "message_id": message.id,
                                "channel_name": panel_channel.name
                            })
                            
                            # Delete the existing panel
                            try:
                                await message.delete()
                                log_operation("delete", "INFO", {
                                    "component": "create_panel",
                                    "action": "existing_panel_deleted",
                                    "message_id": message.id,
                                    "channel_name": panel_channel.name
                                })
                            except Exception as e:
                                log_operation("delete", "WARNING", {
                                    "component": "create_panel",
                                    "action": "panel_deletion_failed",
                                    "message_id": message.id,
                                    "error": str(e)
                                })
                            
                            break  # Found and deleted the panel, break out of the loop
                except Exception as e:
                    log_operation("check", "WARNING", {
                        "component": "create_panel",
                        "action": "history_check_failed",
                        "error_details": "could_not_check_history",
                        "error": str(e)
                    })
                
                # Create the control panel embed
                embed = discord.Embed(
                    title="🎵 QuranBot Control Panel",
                    description="Welcome to QuranBot! Use the controls below to manage your Quran streaming experience.\n\n\n**📖 Surah Selection**\nChoose any surah from all 114 surahs using the dropdown above. Navigate through pages with the buttons below.\n\n\n**🎤 Reciter Selection**\nSwitch between different reciters while maintaining your current surah position.\n\n\n**Playback Controls**\n• ⏮️ Previous - Go to previous surah\n• ⏭️ Next - Go to next surah\n• 🔁 Loop - Toggle repeat mode\n• 🔀 Shuffle - Toggle random playback\n\n\n**Information**\n• 📋 Credits - View bot information and credits\n\n\n**⚠️ Beta Testing Notice**\nThis bot is currently in beta testing. If you encounter any bugs or issues, please DM <@259725211664908288> to report them. Your feedback helps improve the bot!",
                    color=discord.Color.green()
                )
                
                embed.set_footer(text="QuranBot v2.0.0 • Only works for voice channel users")
                embed.timestamp = discord.utils.utcnow()
                
                # Send the panel with buttons
                view = ControlPanelView(bot)
                message = await panel_channel.send(embed=embed, view=view)
                
                log_operation("success", "INFO", {
                    "component": "create_panel",
                    "action": "panel_created",
                    "channel_name": panel_channel.name,
                    "message_id": message.id
                })
                
            except Exception as e:
                log_operation("error", "ERROR", {
                    "component": "create_panel",
                    "error_details": "panel_creation_failed",
                    "error": str(e),
                    "error_type": type(e).__name__
                }, e)
        
        # Schedule panel creation after bot is ready
        async def delayed_create_panel():
            """Create panel after a delay to ensure bot is fully connected."""
            try:
                log_operation("init", "INFO", {
                    "component": "delayed_create_panel",
                    "delay_seconds": 3
                })
                
                await asyncio.sleep(3)  # Wait 3 seconds for bot to fully connect
                await create_panel()
                
            except Exception as e:
                log_operation("error", "ERROR", {
                    "component": "delayed_create_panel",
                    "error_details": "delayed_panel_creation_failed",
                    "error": str(e),
                    "error_type": type(e).__name__
                }, e)
        
        bot.loop.create_task(delayed_create_panel())
        log_operation("success", "INFO", {
            "component": "setup",
            "action": "delayed_panel_task_created"
        })
        
    except Exception as e:
        log_operation("error", "CRITICAL", {
            "component": "setup",
            "error_details": "setup_failed",
            "error": str(e),
            "error_type": type(e).__name__
        }, e) 