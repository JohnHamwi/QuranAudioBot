# Changelog

All notable changes to QuranBot will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.4.0] - 2025-07-05

### Added

- **Interactive Control Panel**: Complete Discord embed-based control panel with real-time status updates
- **Audio Manager System**: Centralized audio playback management with comprehensive state tracking
- **Rich Presence Integration**: Dynamic Discord Rich Presence showing current Surah with Arabic names and playback timer
- **User Attribution System**: Track and display which user enabled Loop/Shuffle modes with Discord mentions
- **Progress Bar Display**: Visual playback progress bars in control panel with 20-character precision
- **Surah Selection Dropdown**: Paginated dropdown menu with emoji indicators and Arabic descriptions
- **Reciter Selection**: Dynamic reciter switching with automatic audio file discovery
- **Playback Controls**: Previous/Next track buttons with seamless audio transitions
- **Loop & Shuffle Modes**: Toggle controls with user attribution and real-time status updates
- **Search Functionality**: Quick Surah search with fuzzy matching capabilities
- **Error Recovery**: Robust error handling with automatic control panel recreation
- **Real-time Updates**: Live status updates every 5 seconds with progress tracking

### Enhanced

- **Rich Presence Display**: Simplified to show only Surah name (emoji + Arabic) with timer in single line
- **Control Panel Layout**: Clean, organized embed with essential information only
- **Surah Dropdown Format**: Shows "1. Al-Fatiha" format with emoji on left, no duplication
- **Audio State Management**: Comprehensive playback state tracking and synchronization
- **User Experience**: Removed redundant status displays, focused on essential information
- **Error Handling**: Graceful handling of deleted control panel messages with automatic recreation

### Technical Improvements

- **AudioManager Class**: Complete audio playback state management system
- **Control Panel View**: Discord UI components with button interactions and dropdown menus
- **Rich Presence Manager**: FFmpeg integration for audio duration detection and progress tracking
- **Surah Database**: JSON-based Surah information with emojis, Arabic names, and metadata
- **Automatic Discovery**: Dynamic reciter detection from audio folder structure
- **Progress Synchronization**: Coordinated progress updates between Rich Presence and control panel

### User Interface

- **Control Panel Features**:
  - Now Playing display with Surah emoji and name
  - Visual progress bar with current/total time
  - Current reciter information
  - Loop status with user attribution (e.g., "Loop: 🔁 ON - <@user_id>")
  - Shuffle status with user attribution
  - Last activity tracking
- **Rich Presence Features**:
  - Compact display: "🕌 الفاتحة • 02:34 / 05:67"
  - Dynamic states: Starting, Playing, Paused
  - Clean, minimalist design

### Fixed

- **Control Panel Persistence**: Proper handling of message deletion and recreation
- **Progress Bar Accuracy**: Correct timing calculations and display formatting
- **Button Interactions**: All control buttons now properly connected to audio system
- **State Synchronization**: Real-time updates between all components
- **Error Recovery**: Graceful handling of Discord API errors and reconnection

## [1.2.0] - 2025-07-05

### Added

- **Professional project structure**: Reorganized entire project with tools/, docs/, config/, scripts/ directories
- **Enhanced development tools**: Comprehensive testing suite, code formatting, and deployment safety tools
- **Complete error handling**: Added traceback support throughout with enhanced tree_log functions
- **Development environment setup**: Automated virtual environment, ffmpeg installation, and audio file management
- **Production safety framework**: Bulletproof deployment system preventing broken code from reaching VPS

### Changed

- **Project organization**: Moved development tools to tools/ directory for better structure
- **Configuration management**: Centralized config files in config/ directory
- **Documentation structure**: Organized all documentation in docs/ directory
- **Import paths**: Updated all tools to work with new directory structure

### Technical Improvements

- **Automatic path resolution**: All tools work correctly from any directory
- **Comprehensive testing**: 41 tests with 100% success rate validation
- **Code consistency**: Black formatting with 88-character lines and box-style headers
- **Memory management**: Updated memory system with project structure standards

### Added

- **Automated instance detection**: Fully automated prevention of multiple bot instances running simultaneously
- **Automatic instance termination**: Seamlessly detects and stops existing instances without user interaction
- **Bot manager utility**: Command-line tool for easy bot management (start, stop, restart, status)
- **Process monitoring**: Detailed process information including uptime, memory usage, and command details
- **Graceful shutdown handling**: Proper termination with fallback to force kill if needed
- **Enhanced error handling**: Robust process management with comprehensive error logging
- **Structured Discord logging**: Custom logging handler that formats Discord.py logs in beautiful tree style
- **Intelligent log filtering**: Automatically categorizes and formats Discord logs with appropriate icons and context
- **Timestamped logging**: All terminal logs now include timestamps in EST timezone with MM/DD HH:MM AM/PM format
- **Professional log formatting**: Enhanced readability with consistent timestamp prefixes on all log entries
- **Comprehensive file logging**: Automatic logging to organized date-based folder structure
- **Multi-format log files**: Simultaneous logging to .log (text), .json (structured), and -errors.log (errors only) files
- **Date-organized structure**: Logs saved to `logs/YYYY-MM-DD/` folders for easy organization and archival
- **Error isolation**: Separate error log file captures only WARNING, ERROR, CRITICAL, and EXCEPTION level messages

### Security

- **Process isolation**: Prevents conflicts and unexpected behavior from multiple instances
- **Safe termination**: Graceful shutdown with timeout protection to prevent hanging processes

### Dependencies

- **psutil**: Added for advanced process monitoring and management capabilities

## [1.1.0] - 2025-07-05

### Added

- **Extremely structured project organization**: Reorganized entire codebase into proper src/ directory structure
- **Modular package architecture**: Created separate packages for bot/, utils/, and config/
- **Proper Python packaging**: Added **init**.py files for all packages with proper imports
- **Clean entry point**: Created main.py as the single entry point with proper import handling
- **Enhanced version tracking**: Added version information display in structured logging

### Changed

- **File organization**: Moved bot.py to src/bot/main.py for better organization
- **Logging module**: Moved tree_log.py to src/utils/tree_log.py
- **Import structure**: Updated all imports to use proper package structure
- **Entry point**: Changed from bot.py to main.py for cleaner project structure

### Technical Structure

```
├── main.py                    # Main entry point
├── requirements.txt           # Dependencies
├── CHANGELOG.md              # This changelog
├── update_version.py         # Version management tool
├── .env                      # Environment configuration
├── audio/                    # Audio files directory
└── src/                      # Source code package
    ├── __init__.py           # Main package init
    ├── bot/                  # Bot functionality package
    │   ├── __init__.py       # Bot package init
    │   └── main.py           # Main bot implementation
    ├── utils/                # Utilities package
    │   ├── __init__.py       # Utils package init
    │   └── tree_log.py       # Tree-style logging functions
    └── config/               # Configuration package
        └── __init__.py       # Config package init (future use)
```

## [1.0.0] - 2025-07-05

### Added

- **Complete bot rewrite**: Started fresh from ground zero with minimal, clean codebase
- **Tree-style logging system**: Implemented structured logging with symbols (├─, └─) for better readability
- **Modular architecture**: Separated logging functionality into `tree_log.py` module
- **Box-style comments**: Added consistent formatting with `# =============================================================================` headers
- **Environment variable integration**: Proper configuration using .env file with exact ID names
- **Audio playback system**: Basic Discord voice channel connection and MP3 playback
- **Auto-reconnection**: Bot automatically attempts to reconnect if disconnected from voice
- **Progress tracking**: Visual progress indicators for audio playback (current/total format)
- **Error handling**: Comprehensive error logging with tree-style format

### Technical Details

- **Dependencies**: Minimal setup with only discord.py, PyNaCl, and python-dotenv
- **Configuration**: Uses GUILD_ID and TARGET_CHANNEL_ID from .env file
- **Audio source**: Plays from 'audio/Saad Al Ghamdi' folder by default
- **FFmpeg integration**: Configurable FFmpeg path for audio processing

### Files Structure

```
├── bot.py              # Main Discord bot functionality
├── tree_log.py         # Tree-style logging functions
├── requirements.txt    # Minimal dependencies
├── .env               # Environment configuration
├── audio/             # Audio files directory
└── CHANGELOG.md       # This changelog file
```

### Removed

- **Previous complex codebase**: Deleted entire previous implementation that had multiple issues
- **Instance detection**: Removed problematic instance management that was causing startup loops
- **Complex logging**: Replaced with simpler, more readable tree-style logging
- **Excessive dependencies**: Reduced from 20+ packages to just 3 core dependencies

### Fixed

- **Voice connection stability**: Resolved WebSocket 4006 errors with clean reconnection logic
- **FFmpeg path detection**: Proper handling of FFmpeg executable path configuration
- **Startup process**: Eliminated hanging during bot initialization
- **Memory management**: Cleaner resource handling without complex monitoring systems
