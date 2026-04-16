from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import csv

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

    def _score(self, user: UserProfile, song: Song) -> float:
        """Computes a numeric score for a Song against a UserProfile."""
        score = 0.0
        if song.genre == user.favorite_genre:
            score += 2.0
        if song.mood == user.favorite_mood:
            score += 1.0
        score += round(1.0 - abs(song.energy - user.target_energy), 2)
        if user.likes_acoustic and song.acousticness >= 0.7:
            score += 0.5
        return score

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Returns the top-k Song objects sorted by score descending."""
        return sorted(self.songs, key=lambda s: self._score(user, s), reverse=True)[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Returns a human-readable explanation of why a song was recommended."""
        parts = []
        if song.genre == user.favorite_genre:
            parts.append("genre match (+2.0)")
        if song.mood == user.favorite_mood:
            parts.append("mood match (+1.0)")
        energy_score = round(1.0 - abs(song.energy - user.target_energy), 2)
        parts.append(f"energy similarity (+{energy_score})")
        if user.likes_acoustic and song.acousticness >= 0.7:
            parts.append("acoustic bonus (+0.5)")
        return ", ".join(parts)

def load_songs(csv_path: str) -> List[Dict]:
    """Loads songs from a CSV file, converting numeric fields to float."""
    numeric = {"energy", "tempo_bpm", "valence", "danceability", "acousticness"}
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        songs = []
        for row in reader:
            for key in numeric:
                row[key] = float(row[key])
            row["id"] = int(row["id"])
            songs.append(row)
    print(f"Loaded songs: {len(songs)}")
    return songs


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Scores a song against user preferences; returns (score, reasons)."""
    score = 0.0
    reasons = []

    if song["genre"] == user_prefs.get("genre"):
        score += 2.0
        reasons.append("genre match (+2.0)")

    if song["mood"] == user_prefs.get("mood"):
        score += 1.0
        reasons.append("mood match (+1.0)")

    energy_gap = abs(song["energy"] - user_prefs.get("energy", 0.5))
    energy_score = round(1.0 - energy_gap, 2)
    score += energy_score
    reasons.append(f"energy similarity (+{energy_score})")

    if user_prefs.get("likes_acoustic") and song["acousticness"] >= 0.7:
        score += 0.5
        reasons.append("acoustic bonus (+0.5)")

    return round(score, 2), reasons


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Returns the top-k songs sorted by score descending."""
    scored = [(song, *score_song(user_prefs, song)) for song in songs]
    scored.sort(key=lambda x: x[1], reverse=True)
    return [(song, score, ", ".join(reasons)) for song, score, reasons in scored[:k]]