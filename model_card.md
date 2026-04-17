# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

**VibeCheck 1.0**

---

## 2. Intended Use

VibeCheck 1.0 suggests up to 5 songs from a 20-song catalog based on a user's preferred genre, mood, energy level, and whether they enjoy acoustic music. It is designed for classroom exploration of how content-based recommenders work.

---

## 3. How the Model Works

Every song in the catalog gets a score based on how well it matches the user's taste profile. The scoring works like this:

- If the song's genre matches the user's favorite genre, it earns 2 points — the biggest reward, because genre is the strongest signal of taste.
- If the song's mood matches the user's favorite mood, it earns 1 point.
- The song earns up to 1 point based on how close its energy level is to the user's target. A perfect energy match gives the full point; a big gap gives close to zero.
- If the user likes acoustic music and the song is highly acoustic, it earns a 0.5 bonus.

All songs are then ranked from highest to lowest score, and the top 5 are returned with a plain-language explanation of why each one was chosen.

---

## 4. Data

The catalog contains 20 songs stored in `data/songs.csv`. The original 10 starter songs were expanded with 10 additional tracks. Genres represented include pop, lofi, rock, EDM, funk, country, alternative, classical, blues, metal, indie pop, synthwave, jazz, and ambient. Moods include happy, chill, intense, relaxed, moody, focused, sad, and calm. The dataset skews toward Western popular music styles and does not include hip-hop, R&B, reggae, or non-English language genres. Numerical features (energy, valence, danceability, acousticness) are all on a 0.0–1.0 scale.

---

## 5. Strengths

- Works well for users with a clear, dominant genre preference, the genre weight of 2.0 ensures strong matches rise to the top quickly.
- The energy similarity score rewards songs that are "in the zone" rather than just the highest or lowest energy, which feels more natural.
- The acoustic bonus gives users who prefer unplugged sounds a meaningful signal without overriding genre and mood.
- The explanation output makes every recommendation transparent — users can see exactly why each song was chosen.
- The 2nd profile produced the most intuitive results: Library Rain and Midnight Coding ranked 1 and 2 with near-perfect scores.

---

## 6. Limitations and Bias

- Genre dominance: Because genre is worth 2 points and mood is only 1, a song with a matching genre but wrong mood will almost always beat a song with a matching mood but wrong genre. This can feel wrong — a happy jazz song might be a better fit for a happy pop user than a sad pop song.
- Dataset size: With only 20 songs, some profiles (like the 3rd profile with `genre=rock, mood=intense, energy=0.92` ) quickly exhaust exact matches and fall back on energy similarity alone, producing EDM and metal songs that may not feel like "rock."
- No artist diversity logic: The same artist can appear multiple times in the top 5. Neon Echo appears twice for the pop profile.
- Missing features: Lyrics, language, tempo preference, and listening history are not considered at all.
- The dataset reflects mostly English-language Western genres, so users who prefer K-pop, Afrobeats, or Latin music would get poor results.

---

## 7. Evaluation

Three user profiles were tested:

1. **High-Energy Pop Fan** (genre=pop, mood=happy, energy=0.85): Sunrise City scored 3.97 and ranked first — a perfect genre + mood + energy match. Gym Hero ranked second despite being "intense" because the genre match still gave it 2 points. This revealed that genre weight can override mood mismatches.

2. **Chill Lofi Studier** (genre=lofi, mood=chill, energy=0.38, likes_acoustic=True): The top 3 were all lofi tracks with high acousticness. Results felt very accurate and matched intuition well.

3. **Deep Intense Rock** (genre=rock, mood=intense, energy=0.92): Only one rock song exists in the catalog (Storm Runner), so ranks 2–5 were filled by EDM and metal songs that matched on mood and energy but not genre. This exposed the small-catalog limitation clearly.

An experiment was also run where if the genre weight were reduced from 2.0 to 0.5, the energy similarity score would dominate, causing very different genres to cluster together based purely on tempo feel — which would likely feel less accurate.

---

## 8. Future Work

- **Add more songs per genre** so that profiles with niche tastes (rock, blues, classical) get meaningful variety in their top 5.
- **Implement a diversity penalty** that reduces the score of a song if the same artist or genre already appears in the top results, preventing repetitive recommendations.
- **Add tempo preference** to the user profile so users can distinguish between a slow jazz ballad and an upbeat jazz track even within the same genre.
- **Support multi-genre profiles** — real users rarely have a single favorite genre, and allowing a ranked list of preferred genres would make the system much more realistic.

---

## 9. Personal Reflection

Building VibeCheck 1.0 made it clear how much a recommender's behavior is shaped by the weights you choose, not just the features. Changing the genre weight from 2.0 to 0.5 would completely change which songs surface, even though no song data changed at all. That was surprising: the "intelligence" of the system lives almost entirely in those numbers, not in any deep understanding of music.

The most interesting moment was seeing the "Deep Intense Rock" profile fall back on EDM and metal songs. It felt wrong intuitively, but the math was correct, those songs genuinely had the closest energy and mood scores. That gap between "mathematically correct" and "feels right" is exactly where real recommenders invest enormous effort, using collaborative filtering, listening history, and neural embeddings to close it. This project made me much more skeptical of recommendations I receive on real platforms — I now think about what features the algorithm is actually optimizing for, and whose taste the training data reflects.
