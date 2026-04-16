import csv
from typing import List, Dict, Tuple
from dataclasses import dataclass


SCORE_MODES = {
    "balanced": {
        "genre": 1.0,
        "mood": 1.0,
        "energy": 4.0,
        "valence": 1.0,
        "tempo": 1.0,
        "acoustic": 0.5,
    },
    "genre_first": {
        "genre": 2.0,
        "mood": 0.75,
        "energy": 3.0,
        "valence": 1.0,
        "tempo": 1.0,
        "acoustic": 0.5,
    },
    "mood_first": {
        "genre": 0.75,
        "mood": 2.0,
        "energy": 3.0,
        "valence": 1.25,
        "tempo": 1.0,
        "acoustic": 0.5,
    },
    "energy_focused": {
        "genre": 0.5,
        "mood": 0.75,
        "energy": 5.0,
        "valence": 1.0,
        "tempo": 1.5,
        "acoustic": 0.5,
    },
}

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
        recommendations = recommend_songs(
            {
                "genre": user.favorite_genre,
                "mood": user.favorite_mood,
                "energy": user.target_energy,
                "likes_acoustic": user.likes_acoustic,
            },
            [_song_to_dict(song) for song in self.songs],
            k=k,
            mode="balanced",
            diversity_penalty=False,
        )
        return [Song(**song) for song, _, _ in recommendations]

    def explain_recommendation(self, user: UserProfile, song: Song, mode: str = "balanced") -> str:
        """Return a short human-readable explanation for one song."""
        score, reasons = score_song(
            {
                "genre": user.favorite_genre,
                "mood": user.favorite_mood,
                "energy": user.target_energy,
                "likes_acoustic": user.likes_acoustic,
            },
            _song_to_dict(song),
            mode=mode,
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


def score_song(user_prefs: Dict, song: Dict, mode: str = "balanced") -> Tuple[float, List[str]]:
    """Score one song against user preferences and return reasons."""
    score = 0.0
    reasons: List[str] = []
    weights = SCORE_MODES.get(mode, SCORE_MODES["balanced"])

    # Exact category matches
    if song.get("genre") == user_prefs.get("genre"):
        genre_points = weights["genre"]
        score += genre_points
        reasons.append(f"genre match (+{genre_points:.2f})")
    if song.get("mood") == user_prefs.get("mood"):
        mood_points = weights["mood"]
        score += mood_points
        reasons.append(f"mood match (+{mood_points:.2f})")

    # Numeric closeness features
    if "energy" in user_prefs and "energy" in song:
        energy_close = max(0.0, 1.0 - abs(float(song["energy"]) - float(user_prefs["energy"])))
        energy_points = weights["energy"] * energy_close
        score += energy_points
        reasons.append(f"energy closeness (+{energy_points:.2f})")

    target_valence = user_prefs.get("target_valence")
    if target_valence is not None and "valence" in song:
        valence_close = max(0.0, 1.0 - abs(float(song["valence"]) - float(target_valence)))
        valence_points = weights["valence"] * valence_close
        score += valence_points
        reasons.append(f"valence closeness (+{valence_points:.2f})")

    target_tempo = user_prefs.get("target_tempo_bpm")
    if target_tempo is not None and "tempo_bpm" in song:
        tempo_close = max(0.0, 1.0 - (abs(float(song["tempo_bpm"]) - float(target_tempo)) / 80.0))
        tempo_points = weights["tempo"] * tempo_close
        score += tempo_points
        reasons.append(f"tempo closeness (+{tempo_points:.2f})")

    likes_acoustic = user_prefs.get("likes_acoustic")
    if likes_acoustic is not None and "acousticness" in song:
        is_acoustic_song = float(song["acousticness"]) >= 0.6
        if bool(likes_acoustic) == is_acoustic_song:
            acoustic_points = weights["acoustic"]
            score += acoustic_points
            reasons.append(f"acoustic preference match (+{acoustic_points:.2f})")

    if not reasons:
        reasons.append("no direct matches; scored by numeric similarity")

    return score, reasons

def _diversity_penalty(song: Dict, selected_songs: List[Dict]) -> Tuple[float, List[str]]:
    """Apply a simple penalty when artist or genre already appears in the shortlist."""
    penalty = 0.0
    reasons: List[str] = []
    selected_artists = [item["artist"] for item in selected_songs]
    selected_genres = [item["genre"] for item in selected_songs]

    artist_count = selected_artists.count(song.get("artist"))
    if artist_count > 0:
        artist_penalty = 0.75 * artist_count
        penalty -= artist_penalty
        reasons.append(f"artist diversity penalty (-{artist_penalty:.2f})")

    genre_count = selected_genres.count(song.get("genre"))
    if genre_count > 0:
        genre_penalty = 0.35 * genre_count
        penalty -= genre_penalty
        reasons.append(f"genre diversity penalty (-{genre_penalty:.2f})")

    return penalty, reasons


def recommend_songs(
    user_prefs: Dict,
    songs: List[Dict],
    k: int = 5,
    mode: str = "balanced",
    diversity_penalty: bool = False,
) -> List[Tuple[Dict, float, str]]:
    """Return top-k song recommendations as (song, score, explanation)."""
    scored_rows: List[Dict] = []
    for song in songs:
        score, reasons = score_song(user_prefs, song, mode=mode)
        scored_rows.append({"song": song, "score": score, "reasons": reasons})

    ranked = sorted(scored_rows, key=lambda item: item["score"], reverse=True)
    selected: List[Tuple[Dict, float, str]] = []
    selected_songs: List[Dict] = []

    while ranked and len(selected) < k:
        best_index = 0
        best_adjusted_score = float("-inf")
        best_reasons: List[str] = []

        for index, candidate in enumerate(ranked):
            candidate_song = candidate["song"]
            candidate_score = candidate["score"]
            candidate_reasons = list(candidate["reasons"])

            adjusted_score = candidate_score
            if diversity_penalty:
                penalty, penalty_reasons = _diversity_penalty(candidate_song, selected_songs)
                adjusted_score += penalty
                candidate_reasons.extend(penalty_reasons)

            if adjusted_score > best_adjusted_score:
                best_adjusted_score = adjusted_score
                best_index = index
                best_reasons = candidate_reasons

        chosen = ranked.pop(best_index)
        selected_songs.append(chosen["song"])
        selected.append(
            (
                chosen["song"],
                best_adjusted_score,
                "; ".join(best_reasons),
            )
        )

    return selected
