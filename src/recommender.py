import csv
from typing import List, Dict, Tuple
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return top-k songs ranked by preference score."""
        scored: List[Tuple[Song, float, List[str]]] = []
        for song in self.songs:
            song_dict = _song_to_dict(song)
            score, reasons = score_song(
                {
                    "genre": user.favorite_genre,
                    "mood": user.favorite_mood,
                    "energy": user.target_energy,
                    "likes_acoustic": user.likes_acoustic,
                },
                song_dict,
            )
            scored.append((song, score, reasons))

        ranked = sorted(scored, key=lambda item: item[1], reverse=True)
        return [song for song, _, _ in ranked[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a short human-readable explanation for one song."""
        score, reasons = score_song(
            {
                "genre": user.favorite_genre,
                "mood": user.favorite_mood,
                "energy": user.target_energy,
                "likes_acoustic": user.likes_acoustic,
            },
            _song_to_dict(song),
        )
        return f"Score {score:.2f}: " + "; ".join(reasons)


def _song_to_dict(song: Song) -> Dict:
    """Convert a Song dataclass into a dictionary with expected keys."""
    return {
        "id": song.id,
        "title": song.title,
        "artist": song.artist,
        "genre": song.genre,
        "mood": song.mood,
        "energy": song.energy,
        "tempo_bpm": song.tempo_bpm,
        "valence": song.valence,
        "danceability": song.danceability,
        "acousticness": song.acousticness,
    }

def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from CSV into typed dictionaries for scoring."""
    songs: List[Dict] = []
    int_fields = {"id", "tempo_bpm"}
    float_fields = {"energy", "valence", "danceability", "acousticness"}

    with open(csv_path, mode="r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            typed = dict(row)
            for key in int_fields:
                typed[key] = int(row[key])
            for key in float_fields:
                typed[key] = float(row[key])
            songs.append(typed)

    print(f"Loaded songs: {len(songs)}")
    return songs


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score one song against user preferences and return reasons."""
    score = 0.0
    reasons: List[str] = []

    # Exact category matches
    if song.get("genre") == user_prefs.get("genre"):
        score += 2.0
        reasons.append("genre match (+2.0)")
    if song.get("mood") == user_prefs.get("mood"):
        score += 1.0
        reasons.append("mood match (+1.0)")

    # Numeric closeness features
    if "energy" in user_prefs and "energy" in song:
        energy_close = max(0.0, 1.0 - abs(float(song["energy"]) - float(user_prefs["energy"])))
        energy_points = 2.0 * energy_close
        score += energy_points
        reasons.append(f"energy closeness (+{energy_points:.2f})")

    target_valence = user_prefs.get("target_valence")
    if target_valence is not None and "valence" in song:
        valence_close = max(0.0, 1.0 - abs(float(song["valence"]) - float(target_valence)))
        valence_points = 1.0 * valence_close
        score += valence_points
        reasons.append(f"valence closeness (+{valence_points:.2f})")

    target_tempo = user_prefs.get("target_tempo_bpm")
    if target_tempo is not None and "tempo_bpm" in song:
        tempo_close = max(0.0, 1.0 - (abs(float(song["tempo_bpm"]) - float(target_tempo)) / 80.0))
        tempo_points = 1.0 * tempo_close
        score += tempo_points
        reasons.append(f"tempo closeness (+{tempo_points:.2f})")

    likes_acoustic = user_prefs.get("likes_acoustic")
    if likes_acoustic is not None and "acousticness" in song:
        is_acoustic_song = float(song["acousticness"]) >= 0.6
        if bool(likes_acoustic) == is_acoustic_song:
            score += 0.5
            reasons.append("acoustic preference match (+0.5)")

    if not reasons:
        reasons.append("no direct matches; scored by numeric similarity")

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Return top-k song recommendations as (song, score, explanation)."""
    scored_rows: List[Tuple[Dict, float, List[str]]] = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        scored_rows.append((song, score, reasons))

    ranked = sorted(scored_rows, key=lambda item: item[1], reverse=True)
    top_k = ranked[:k]

    return [
        (song, score, "; ".join(reasons))
        for song, score, reasons in top_k
    ]
