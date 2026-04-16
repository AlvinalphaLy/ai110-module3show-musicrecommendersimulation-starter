# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

VibeFinder 1.0

---

## 2. Goal / Task

This model suggests songs from a small catalog.
It tries to match a user’s taste profile.
It is for classroom exploration, not real users.

---

## 3. Data Used

The dataset has 18 songs in `data/songs.csv`.
Each song has genre, mood, energy, tempo, valence, danceability, and acousticness.
The catalog is small, so it does not cover every kind of music taste.
It also reflects the styles I added to the starter set.

---

## 4. Algorithm Summary

The recommender gives points for matches.
It rewards the same genre and mood as the user.
It also rewards songs that are close in energy, valence, tempo, and acousticness.
Songs with the highest total score are recommended first.

---

## 5. Observed Behavior / Biases

The model can over-favor songs that match several strong signals at once.
It can also keep recommending the same songs because the catalog is small.
The dataset has more chill and acoustic songs than some other styles.
That can make the results less balanced for users who want harder or stranger combinations.
The model does not understand lyrics, language, or listening history.

---

## 6. Evaluation Process

I tested four profiles: High-Energy Pop, Chill Lofi, Deep Intense Rock, and a conflicting edge case.
I compared the top five songs for each profile.
I also tried a weight shift where energy mattered more and genre mattered less.
That made the results feel more responsive to mood and tempo.
It also made the ranking a little less stable.

---

## 7. Intended Use and Non-Intended Use

This model is meant for a classroom demo.
It is useful for showing how scoring rules turn data into recommendations.
It should not be used for real music product decisions.
It should not be used to predict real user behavior or fairness.

---

## 8. Ideas for Improvement

I would add more songs.
I would add a diversity rule so the top results are less repetitive.
I would also add more user features, like language or genre ranges.

---

## 9. Personal Reflection

My biggest learning moment was seeing how simple rules can still feel like real recommendations.
AI tools helped me test ideas quickly and spot bias patterns faster.
I still had to double-check the outputs, because a good explanation does not always mean the ranking is balanced.
What surprised me most was how a small scoring change could shift the whole list.
If I extended this project, I would try more profiles and add diversity controls.
