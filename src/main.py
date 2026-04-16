"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs


PROFILES = {
    "High-Energy Pop Fan": {"genre": "pop", "mood": "happy", "energy": 0.85, "likes_acoustic": False},
    "Chill Lofi Studier":  {"genre": "lofi", "mood": "chill", "energy": 0.38, "likes_acoustic": True},
    "Deep Intense Rock":   {"genre": "rock", "mood": "intense", "energy": 0.92, "likes_acoustic": False},
}


def main() -> None:
    songs = load_songs("data/songs.csv")

    for profile_name, user_prefs in PROFILES.items():
        print(f"\n{'='*50}")
        print(f"Profile: {profile_name}")
        print(f"Prefs: genre={user_prefs['genre']}, mood={user_prefs['mood']}, "
              f"energy={user_prefs['energy']}, likes_acoustic={user_prefs['likes_acoustic']}")
        print(f"{'='*50}")
        recommendations = recommend_songs(user_prefs, songs, k=5)
        for rank, (song, score, explanation) in enumerate(recommendations, 1):
            print(f"{rank}. {song['title']} by {song['artist']}  |  Score: {score:.2f}")
            print(f"   Because: {explanation}")


if __name__ == "__main__":
    main()
