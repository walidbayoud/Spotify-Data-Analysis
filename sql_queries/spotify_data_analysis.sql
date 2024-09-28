-- =======================
-- Spotify Data Analysis
-- =======================
 
-- INDEX CREATION FOR PERFORMANCE OPTIMIZATION --
-- ------------------------------------------------
-- Create indexes to improve query performance.
CREATE INDEX idx_views ON spotify(views);
CREATE INDEX idx_artist ON spotify(artist);
CREATE INDEX idx_track ON spotify(track);
CREATE INDEX idx_album ON spotify(album);
CREATE INDEX idx_most_played_on ON spotify(most_played_on);
CREATE INDEX idx_liveness ON spotify(liveness);
CREATE INDEX idx_energy ON spotify(energy);
CREATE INDEX idx_danceability ON spotify(danceability);

-- =======================
-- 1. Correlation Between Audio Features and Engagement Metrics
-- =======================
-- Query to analyze correlations between audio features (energy, danceability, tempo, valence) 
-- and engagement metrics (likes, views, streams).

SELECT 
    CORR(energy, views) AS energy_views_corr,
    CORR(energy, likes) AS energy_likes_corr,
    CORR(energy, stream) AS energy_stream_corr,
    CORR(danceability, views) AS danceability_views_corr,
    CORR(danceability, likes) AS danceability_likes_corr,
    CORR(danceability, stream) AS danceability_stream_corr,
    CORR(tempo, views) AS tempo_views_corr,
    CORR(tempo, likes) AS tempo_likes_corr,
    CORR(tempo, stream) AS tempo_stream_corr,
    CORR(valence, views) AS valence_views_corr,
    CORR(valence, likes) AS valence_likes_corr,
    CORR(valence, stream) AS valence_stream_corr
FROM spotify;

-- =======================
-- 2. High-Engagement Tracks Needing Promotion
-- =======================
-- Query to find tracks that have high engagement (likes/views) but lower views, 
-- indicating potential candidates for promotion.

WITH avg_metrics AS (
    SELECT AVG(energy) AS avg_energy, 
           AVG(danceability) AS avg_danceability,
           AVG(views) AS avg_views
    FROM spotify
)
SELECT track, artist, album, 
       energy, danceability, views, likes,
       CASE WHEN views > 0 THEN likes / views ELSE 0 END AS engagement_rate
FROM spotify, avg_metrics
WHERE energy > avg_metrics.avg_energy
  AND danceability > avg_metrics.avg_danceability
  AND views BETWEEN 50000 AND 150000
ORDER BY energy DESC, danceability DESC;

-- =======================
-- 3. Best Performing Platform for Each Artist
-- =======================
-- Query to compare performance between YouTube and Spotify for the top 50 artists.

WITH artist_ranking AS (
    SELECT artist, SUM(views) AS total_views
    FROM spotify
    GROUP BY artist
    ORDER BY total_views DESC
    LIMIT 50
),
platform_performance AS (
    SELECT artist_ranking.artist,
           SUM(CASE WHEN most_played_on = 'Youtube' THEN stream END) AS youtube_streams,
           SUM(CASE WHEN most_played_on = 'Spotify' THEN stream END) AS spotify_streams,
           SUM(CASE WHEN most_played_on = 'Youtube' THEN likes END) AS youtube_likes,
           SUM(CASE WHEN most_played_on = 'Spotify' THEN likes END) AS spotify_likes,
           SUM(CASE WHEN most_played_on = 'Youtube' THEN comments END) AS youtube_comments,
           SUM(CASE WHEN most_played_on = 'Spotify' THEN comments END) AS spotify_comments,
           COUNT(CASE WHEN most_played_on = 'Youtube' THEN track END) AS youtube_track_count,
           COUNT(CASE WHEN most_played_on = 'Spotify' THEN track END) AS spotify_track_count
    FROM spotify
    JOIN artist_ranking ON spotify.artist = artist_ranking.artist
    GROUP BY artist_ranking.artist
)
SELECT artist, youtube_streams, spotify_streams, youtube_likes, spotify_likes,
       youtube_comments, spotify_comments, youtube_track_count, spotify_track_count
FROM platform_performance
ORDER BY spotify_streams DESC, youtube_streams DESC;

-- =======================
-- 4. Top 3 Most-Viewed Tracks for Each Artist (Window Functions)
-- =======================
-- Query to rank and retrieve the top 3 most-viewed tracks for each artist using window functions.

WITH ranking_artist AS (
    SELECT artist, track, SUM(views) AS total_view,
           DENSE_RANK() OVER (PARTITION BY artist ORDER BY SUM(views) DESC) AS rank
    FROM spotify
    GROUP BY artist, track
)
SELECT * 
FROM ranking_artist
WHERE rank <= 3
ORDER BY artist, total_view DESC;

-- =======================
-- 5. Tracks with Above-Average Liveness
-- =======================
-- Query to find tracks where the liveness score is above average.

SELECT track, liveness
FROM spotify
WHERE liveness > (SELECT AVG(liveness) FROM spotify)
ORDER BY liveness DESC;

-- =======================
-- 6. Cumulative Sum of Likes by Views
-- =======================
-- Query to calculate the cumulative sum of likes for tracks ordered by the number of views using window functions.

SELECT track, views, COALESCE(likes, 0) AS likes,
       SUM(COALESCE(likes, 0)) OVER (ORDER BY views DESC ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS cumulative_likes
FROM spotify
ORDER BY views DESC;
