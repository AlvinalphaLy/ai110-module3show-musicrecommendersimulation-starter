"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from .recommender import load_songs, recommend_songs
from textwrap import shorten, wrap


USER_PROFILES = [
    (
        "High-Energy Pop",
        "genre_first",
        {
            "favorite_genre": "pop",
            "favorite_mood": "happy",
            "target_energy": 0.88,
            "target_valence": 0.82,
            "target_tempo_bpm": 128,
            "likes_acoustic": False,
        },
    ),
    (
        "Chill Lofi",
        "mood_first",
        {
            "favorite_genre": "lofi",
            "favorite_mood": "chill",
            "target_energy": 0.40,
            "target_valence": 0.58,
            "target_tempo_bpm": 80,
            "likes_acoustic": True,
        },
    ),
    (
        "Deep Intense Rock",
        "energy_focused",
        {
            "favorite_genre": "rock",
            "favorite_mood": "intense",
            "target_energy": 0.92,
            "target_valence": 0.46,
            "target_tempo_bpm": 150,
            "likes_acoustic": False,
        },
    ),
    (
        "Conflicting Edge Case",
        "balanced",
        {
            "favorite_genre": "classical",
            "favorite_mood": "sad",
            "target_energy": 0.90,
            "target_valence": 0.30,
            "target_tempo_bpm": 160,
            "likes_acoustic": True,
        },
    ),
]


def _print_recommendations(title: str, mode: str, user_prefs: dict, songs: list) -> None:
    recommendations = recommend_songs(user_prefs, songs, k=5, mode=mode, diversity_penalty=True)
    table_width = 120
    title_line = f"{title} [{mode.replace('_', ' ').title()}]"
    print(f"\n{title_line}")
    print("=" * min(table_width, max(len(title_line), 24)))
    print(f"| {'Rank':<4} | {'Title':<22} | {'Artist':<18} | {'Score':<7} | Reasons")
    print("|" + "-" * (table_width - 2) + "|")

    for rank, rec in enumerate(recommendations, start=1):
        song, score, explanation = rec
        title_text = shorten(song['title'], width=22, placeholder="...")
        artist_text = shorten(song['artist'], width=18, placeholder="...")
        reason_lines = wrap(explanation, width=table_width - 42) or [""]
        first_reason = reason_lines[0]
        print(f"| {rank:<4} | {title_text:<22} | {artist_text:<18} | {score:<7.2f} | {first_reason}")
        for reason_line in reason_lines[1:]:
            print(f"| {'':<4} | {'':<22} | {'':<18} | {'':<7} | {reason_line}")
        print("|" + "-" * (table_width - 2) + "|")


def main() -> None:
    songs = load_songs("data/songs.csv")

    print("Scoring modes: balanced, genre_first, mood_first, energy_focused")
    for title, mode, user_prefs in USER_PROFILES:
        _print_recommendations(title, mode, user_prefs, songs)


if __name__ == "__main__":
    main()
