# =============================================================================
# QuranBot - Surah Mapping Module
# =============================================================================
# Maps Surah numbers (1-114) to names, emojis, and metadata
# Provides beautiful display formatting for Discord and logging
# =============================================================================

import json
import os
import random
import traceback
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Tuple

try:
    from .tree_log import (
        log_critical_error,
        log_error_with_traceback,
        log_tree,
        log_warning_with_context,
    )
except ImportError:
    # Fallback for direct execution
    import sys

    sys.path.append(os.path.dirname(__file__))
    from tree_log import (
        log_critical_error,
        log_error_with_traceback,
        log_tree,
        log_warning_with_context,
    )

# =============================================================================
# Surah Data Classes and Enums
# =============================================================================


class RevelationType(Enum):
    """Type of revelation location"""

    MECCAN = "Meccan"
    MEDINAN = "Medinan"


@dataclass
class SurahInfo:
    """Complete information about a Surah"""

    number: int
    name_arabic: str
    name_english: str
    name_transliteration: str
    emoji: str
    verses: int
    revelation_type: RevelationType
    meaning: str
    description: str


# =============================================================================
# JSON Data Loading
# =============================================================================


def load_surah_database() -> Dict[int, SurahInfo]:
    """Load Surah database from JSON file"""
    json_path = Path(__file__).parent / "surahs.json"

    log_tree("📖 Loading Surah database from JSON")

    try:
        if not json_path.exists():
            log_critical_error(
                "surahs.json file not found",
                f"Expected path: {json_path}",
                "surah_mapper",
            )
            return {}

        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        log_tree(f"📊 Loaded {len(data)} Surahs from JSON")

        database = {}
        for number_str, surah_data in data.items():
            try:
                number = int(number_str)

                # Validate required fields
                required_fields = [
                    "number",
                    "name_arabic",
                    "name_english",
                    "name_transliteration",
                    "emoji",
                    "verses",
                    "revelation_type",
                    "meaning",
                    "description",
                ]

                missing_fields = [
                    field for field in required_fields if field not in surah_data
                ]
                if missing_fields:
                    log_warning_with_context(
                        f"Surah {number} missing fields: {missing_fields}",
                        f"Skipping Surah {number}",
                        "surah_mapper",
                    )
                    continue

                database[number] = SurahInfo(
                    number=surah_data["number"],
                    name_arabic=surah_data["name_arabic"],
                    name_english=surah_data["name_english"],
                    name_transliteration=surah_data["name_transliteration"],
                    emoji=surah_data["emoji"],
                    verses=surah_data["verses"],
                    revelation_type=RevelationType(surah_data["revelation_type"]),
                    meaning=surah_data["meaning"],
                    description=surah_data["description"],
                )

            except (ValueError, KeyError, TypeError) as e:
                log_error_with_traceback(f"Error processing Surah {number_str}", e)
                continue

        if len(database) == 114:
            log_tree(f"✅ Successfully loaded all 114 Surahs")
        else:
            log_warning_with_context(
                f"Only loaded {len(database)}/114 Surahs",
                "Some Surahs may be missing or invalid",
                "surah_mapper",
            )

        return database

    except json.JSONDecodeError as e:
        log_error_with_traceback(
            "Invalid JSON format in surahs.json",
            f"JSON decode error: {str(e)}",
            "surah_mapper",
        )
        return {}

    except FileNotFoundError as e:
        log_critical_error("Surah database file not found", f"File path: {json_path}")
        return {}

    except PermissionError as e:
        log_error_with_traceback("Permission denied reading surahs.json", e)
        return {}

    except Exception as e:
        log_critical_error(
            "Unexpected error loading Surah database",
            f"Error: {str(e)}\nTraceback: {traceback.format_exc()}",
            "surah_mapper",
        )
        return {}


# Load the database once when module is imported
SURAH_DATABASE = load_surah_database()

# =============================================================================
# Utility Functions
# =============================================================================


def get_surah_info(surah_number: int) -> Optional[SurahInfo]:
    """Get complete information about a Surah by number"""
    try:
        if not validate_surah_number(surah_number):
            log_warning_with_context(
                f"Invalid Surah number: {surah_number}", "Valid range is 1-114"
            )
            return None

        if not SURAH_DATABASE:
            log_critical_error(
                "Surah database not loaded", "Cannot retrieve Surah information"
            )
            return None

        return SURAH_DATABASE.get(surah_number)

    except Exception as e:
        log_error_with_traceback(
            f"Error getting Surah info for number {surah_number}", e
        )
        return None


def get_surah_name(
    surah_number: int, include_emoji: bool = True, language: str = "english"
) -> str:
    """Get formatted Surah name"""
    try:
        surah = get_surah_info(surah_number)
        if not surah:
            log_tree(f"⚠️ Surah {surah_number} not found, using fallback")
            return f"Surah {surah_number}"

        if language == "arabic":
            name = surah.name_arabic
        elif language == "transliteration":
            name = surah.name_transliteration
        else:  # english
            name = surah.name_english

        if include_emoji:
            return f"{surah.emoji} {name}"
        return name

    except Exception as e:
        log_error_with_traceback(f"Error formatting Surah name for {surah_number}", e)
        return f"Surah {surah_number}"


def get_surah_display(surah_number: int, format_type: str = "full") -> str:
    """Get formatted display string for a Surah"""
    try:
        surah = get_surah_info(surah_number)
        if not surah:
            log_tree(f"⚠️ Surah {surah_number} not found, using fallback")
            return f"Surah {surah_number}"

        if format_type == "short":
            return f"{surah.emoji} {surah.name_english}"
        elif format_type == "number":
            return f"{surah_number:03d}. {surah.emoji} {surah.name_english}"
        elif format_type == "detailed":
            return (
                f"{surah_number:03d}. {surah.emoji} {surah.name_english} "
                f"({surah.name_transliteration}) - {surah.verses} verses"
            )
        else:  # full
            return (
                f"{surah_number:03d}. {surah.emoji} {surah.name_english} "
                f"({surah.name_transliteration})"
            )

    except Exception as e:
        log_error_with_traceback(
            f"Error formatting Surah display for {surah_number}", e
        )
        return f"Surah {surah_number}"


def get_random_surah() -> Optional[SurahInfo]:
    """Get a random Surah"""
    try:
        if not SURAH_DATABASE:
            log_critical_error("Cannot get random Surah", "Database not loaded")
            return None

        surah = random.choice(list(SURAH_DATABASE.values()))
        log_tree(f"🎲 Selected random Surah: {surah.name_english}")
        return surah

    except Exception as e:
        log_error_with_traceback("Error getting random Surah", e)
        return None


def search_surahs(query: str) -> List[SurahInfo]:
    """Search for Surahs by name (English, Arabic, or transliteration)"""
    try:
        if not query or not query.strip():
            log_warning_with_context(
                "Empty search query provided", "Returning empty results"
            )
            return []

        if not SURAH_DATABASE:
            log_critical_error("Cannot search Surahs", "Database not loaded")
            return []

        query = query.lower().strip()
        results = []

        for surah in SURAH_DATABASE.values():
            if (
                query in surah.name_english.lower()
                or query in surah.name_transliteration.lower()
                or query in surah.name_arabic
            ):
                results.append(surah)

        log_tree(f"🔍 Search '{query}' found {len(results)} Surahs")
        return results

    except Exception as e:
        log_error_with_traceback(f"Error searching Surahs with query '{query}'", e)
        return []


def get_meccan_surahs() -> List[SurahInfo]:
    """Get all Meccan Surahs"""
    try:
        if not SURAH_DATABASE:
            log_critical_error("Cannot get Meccan Surahs", "Database not loaded")
            return []

        meccan = [
            s
            for s in SURAH_DATABASE.values()
            if s.revelation_type == RevelationType.MECCAN
        ]
        log_tree(f"🕌 Found {len(meccan)} Meccan Surahs")
        return meccan

    except Exception as e:
        log_error_with_traceback("Error getting Meccan Surahs", e)
        return []


def get_medinan_surahs() -> List[SurahInfo]:
    """Get all Medinan Surahs"""
    try:
        if not SURAH_DATABASE:
            log_critical_error("Cannot get Medinan Surahs", "Database not loaded")
            return []

        medinan = [
            s
            for s in SURAH_DATABASE.values()
            if s.revelation_type == RevelationType.MEDINAN
        ]
        log_tree(f"🏛️ Found {len(medinan)} Medinan Surahs")
        return medinan

    except Exception as e:
        log_error_with_traceback("Error getting Medinan Surahs", e)
        return []


def get_short_surahs(max_verses: int = 20) -> List[SurahInfo]:
    """Get Surahs with fewer than specified verses"""
    try:
        if not SURAH_DATABASE:
            log_critical_error("Cannot get short Surahs", "Database not loaded")
            return []

        short = [s for s in SURAH_DATABASE.values() if s.verses <= max_verses]
        log_tree(f"📜 Found {len(short)} Surahs with ≤{max_verses} verses")
        return short

    except Exception as e:
        log_error_with_traceback(
            f"Error getting short Surahs (max_verses={max_verses})", e
        )
        return []


def get_long_surahs(min_verses: int = 100) -> List[SurahInfo]:
    """Get Surahs with more than specified verses"""
    try:
        if not SURAH_DATABASE:
            log_critical_error("Cannot get long Surahs", "Database not loaded")
            return []

        long = [s for s in SURAH_DATABASE.values() if s.verses >= min_verses]
        log_tree(f"📚 Found {len(long)} Surahs with ≥{min_verses} verses")
        return long

    except Exception as e:
        log_error_with_traceback(
            f"Error getting long Surahs (min_verses={min_verses})", e
        )
        return []


def validate_surah_number(surah_number: int) -> bool:
    """Validate if a Surah number is valid (1-114)"""
    try:
        is_valid = 1 <= surah_number <= 114
        if not is_valid:
            log_tree(f"❌ Invalid Surah number: {surah_number} (valid: 1-114)")
        return is_valid

    except Exception as e:
        log_error_with_traceback(f"Error validating Surah number {surah_number}", e)
        return False


def get_surah_stats() -> Dict[str, int]:
    """Get statistics about the Quran"""
    try:
        if not SURAH_DATABASE:
            log_critical_error("Cannot get Surah statistics", "Database not loaded")
            return {}

        meccan_count = len(get_meccan_surahs())
        medinan_count = len(get_medinan_surahs())
        total_verses = sum(s.verses for s in SURAH_DATABASE.values())

        stats = {
            "total_surahs": len(SURAH_DATABASE),
            "meccan_surahs": meccan_count,
            "medinan_surahs": medinan_count,
            "total_verses": total_verses,
            "shortest_surah": min(
                SURAH_DATABASE.values(), key=lambda s: s.verses
            ).verses,
            "longest_surah": max(
                SURAH_DATABASE.values(), key=lambda s: s.verses
            ).verses,
        }

        log_tree(f"📊 Generated Quran statistics: {len(stats)} metrics")
        return stats

    except Exception as e:
        log_error_with_traceback("Error generating Surah statistics", e)
        return {}


# =============================================================================
# Discord Formatting Functions
# =============================================================================


def format_now_playing(surah_number: int, reciter: str = "Saad Al Ghamdi") -> str:
    """Format 'now playing' message for Discord"""
    try:
        surah = get_surah_info(surah_number)
        if not surah:
            log_tree(f"⚠️ Using fallback format for Surah {surah_number}")
            return f"🎵 Now Playing: Surah {surah_number} by {reciter}"

        formatted = (
            f"🎵 **Now Playing**\n"
            f"{surah.emoji} **{surah.name_english}** ({surah.name_transliteration})\n"
            f"📖 Surah {surah_number} • {surah.verses} verses • {surah.revelation_type.value}\n"
            f"🎤 Recited by **{reciter}**"
        )

        log_tree(f"🎵 Formatted Discord message for {surah.name_english}")
        return formatted

    except Exception as e:
        log_error_with_traceback(
            f"Error formatting 'now playing' for Surah {surah_number}", e
        )
        return f"🎵 Now Playing: Surah {surah_number} by {reciter}"


def format_surah_info_embed(surah_number: int) -> Dict[str, str]:
    """Format Surah information for Discord embed"""
    try:
        surah = get_surah_info(surah_number)
        if not surah:
            log_tree(f"⚠️ Using fallback embed for Surah {surah_number}")
            return {
                "title": f"Surah {surah_number}",
                "description": "Information not available",
            }

        embed_data = {
            "title": f"{surah.emoji} {surah.name_english} ({surah.name_transliteration})",
            "description": surah.description,
            "fields": [
                {"name": "Arabic Name", "value": surah.name_arabic, "inline": True},
                {"name": "Number", "value": str(surah.number), "inline": True},
                {"name": "Verses", "value": str(surah.verses), "inline": True},
                {
                    "name": "Revelation",
                    "value": surah.revelation_type.value,
                    "inline": True,
                },
                {"name": "Meaning", "value": surah.meaning, "inline": True},
            ],
        }

        log_tree(f"📋 Formatted Discord embed for {surah.name_english}")
        return embed_data

    except Exception as e:
        log_error_with_traceback(f"Error formatting embed for Surah {surah_number}", e)
        return {
            "title": f"Surah {surah_number}",
            "description": "Error loading information",
        }


# =============================================================================
# Example Usage and Testing
# =============================================================================

if __name__ == "__main__":
    # Test the mapper
    log_tree(f"🕌 QuranBot Surah Mapper Test")
    print("=" * 50)

    # Check if database loaded successfully
    if not SURAH_DATABASE:
        log_critical_error(
            "Failed to load Surah database!", "Cannot proceed with tests"
        )
        exit(1)

    # Test specific Surahs
    test_surahs = [1, 2, 36, 55, 112, 114]

    for num in test_surahs:
        info = get_surah_info(num)
        if info:
            print(f"\n{get_surah_display(num, 'detailed')}")
            print(f"   Meaning: {info.meaning}")
            print(f"   Type: {info.revelation_type.value}")

    # Test search
    print(f"\n\nSearch Results for 'light':")
    results = search_surahs("light")
    for surah in results:
        print(f"  {get_surah_display(surah.number)}")

    # Test stats
    stats = get_surah_stats()
    print(f"\n\nQuran Statistics:")
    for key, value in stats.items():
        print(f"  {key.replace('_', ' ').title()}: {value}")

    # Test formatting
    print(f"\n\nNow Playing Format:")
    print(format_now_playing(36, "Saad Al Ghamdi"))

    log_tree(f"✅ All tests completed successfully")
