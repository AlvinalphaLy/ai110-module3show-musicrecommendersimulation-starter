# Evaluation Reflection

High-Energy Pop and Deep Intense Rock did not behave the same way even though both wanted fast, energetic songs. The pop profile still leaned toward songs that matched the happy mood and mainstream genre signal, while the rock profile pulled harder toward the fastest, most aggressive tracks because the genre and mood cues lined up differently.

Chill Lofi and the conflicting edge case showed the biggest difference in output shape. Chill Lofi stayed clustered around slower, more acoustic songs, which makes sense because its preferences point to calm music with a lower tempo. The conflicting profile looked more mixed because the high energy target fought against the sad and classical preferences, so the recommender had to balance incompatible signals instead of following one obvious lane.

Gym Hero kept showing up for upbeat pop profiles because the catalog is small and the song matches several strong signals at once: pop genre, intense energy, and a tempo close to a workout-friendly target. That makes it a good example of how a recommender can look “stuck” when one track fits many of the same rules better than the rest of the dataset.

Pairwise comparison notes:

- High-Energy Pop vs Chill Lofi: the pop profile favored brighter, more club-ready songs, while the lofi profile shifted toward slower and softer tracks with more acoustic texture.
- High-Energy Pop vs Deep Intense Rock: both wanted energy, but the rock profile pushed harder toward aggressive songs with heavier tempo and mood signals.
- High-Energy Pop vs Conflicting Edge Case: the conflicting profile did not lock onto the same upbeat pop results because the classical and sad preferences pulled the ranking away from happy mainstream tracks.
- Chill Lofi vs Deep Intense Rock: the lofi profile concentrated on calm tracks, while the rock profile jumped to songs with much higher intensity and tempo.
- Chill Lofi vs Conflicting Edge Case: both liked some acoustic songs, but the conflicting profile was less consistent because its high energy request pulled against the slow, relaxed sound.
- Deep Intense Rock vs Conflicting Edge Case: the rock profile strongly preferred heavy and fast songs, while the conflicting profile scattered more because it mixed opposite signals.
