# Spotify Data Analysis

![spotify_logo](https://github.com/user-attachments/assets/9e7b670c-6deb-49cf-80b0-cb4866b2ed24)


## Executive Summary

This project analyzes the relationship between Spotify track characteristics (such as energy, danceability, tempo, and valence) and engagement metrics (likes, views, streams). 

Key findings include:
- **Energy & Streams**: Tracks with high energy levels don't necessarily have more streams, showing a weak correlation.
- **Danceability & Likes**: Tracks that are more danceable tend to receive more likes.
- **High Engagement, Low Views**: Some tracks, despite having high engagement, are not widely viewed and could benefit from additional promotion.
- **Spotify vs YouTube**: In most cases, artists perform better on Spotify than on YouTube, with a few exceptions.

---

## Introduction

This project delves into how Spotify tracks' audio features, such as energy, danceability, tempo, and valence, influence user engagement metrics like likes, views, and streams. We aim to uncover patterns in user interaction, identify tracks with high engagement but low visibility, and compare platform performance for top artists (YouTube vs Spotify).

The analysis is structured around the following objectives:
- **Audio Feature Correlations**: Investigating how different track features correlate with engagement metrics.
- **Tracks Needing Promotion**: Identifying high-engagement tracks that have low view counts and may benefit from promotion.
- **Platform Performance**: Comparing streaming numbers for top artists on both YouTube and Spotify.

## Metadata

- **Dataset Source**: The dataset used in this project was downloaded from Kaggle ([Spotify Dataset](https://www.kaggle.com/datasets/sanjanchaudhari/spotify-dataset/data)) and contains detailed information about Spotify tracks, including audio features and engagement metrics.
- **Files in the Project**:
  - `data/`: Contains the raw and cleaned data files used for the analysis.
  - `scripts/`: Contains Python scripts used to perform analysis and generate visualizations.
  - `sql_queries/`: SQL scripts for extracting and processing data.
  - `visualizations/`: Contains images of the plots and charts generated from the analysis.

  
## Tech Stack

- **SQL**: For querying and analyzing data from the dataset.
- **Python**: For further analysis, processing, and visualization (libraries used include Pandas, Matplotlib, and Seaborn).
- **GitHub**: For version control and project management.
- **Jupyter Notebook** (optional): For exploring data and presenting visual analysis interactively.

---

## Question 1: How do audio features (energy, danceability, tempo, valence) affect engagement metrics (likes, views, streams)?
### Goal: To calculate the correlation between various audio features (energy, danceability, tempo, valence) and engagement metrics (likes, views, streams) and visualize the correlation matrix using a heatmap.
### SQL Query
This query calculates the correlation between various audio features (energy, danceability, tempo, valence) and engagement metrics (views, likes, streams).
```sql
-- SQL Query to calculate correlation between audio features and engagement metrics
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
```
### Query Results:
The results of the SQL query can be found in the spotify_data_1.csv file located in the `data/` folder.
[spotify_data_1.csv](data/spotify_data_1.csv)


| Audio Feature   | Views Correlation | Likes Correlation | Streams Correlation |
|-----------------|-------------------|-------------------|---------------------|
| Energy          | 0.065              | 0.06              | 0.04                |
| Danceability    | 0.087              | 0.098             | 0.072               |
| Tempo           | -0.0014            | 0.0024            | 0.0019              |
| Valence         | 0.034              | 0.0096            | -0.015              |



### Python Script
This script calculates the correlation between various audio features (energy, danceability, tempo, valence) and engagement metrics (likes, views, streams). It then generates a heatmap to visually represent the correlation between these metrics.
```python
# audio_correlation_analysis.py

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the CSV file
df = pd.read_csv('../data/spotify_data_1.csv')

# Select the relevant columns for correlation analysis
columns_to_analyze = ['energy', 'danceability', 'tempo', 'valence', 'views', 'likes', 'stream']
df_corr = df[columns_to_analyze]

# Calculate the correlation matrix
correlation_matrix = df_corr.corr()

# Create the heatmap for correlations
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap="#1DB954", linewidths=0.5)

# Add title and show plot
plt.title('Correlation Between Audio Features and Engagement Metrics')
plt.savefig('../visualizations/correlation_heatmap.png')
plt.show()
```
[audio_correlation_analysis.py](scripts/audio_correlation_analysis.py)

## Visualization

![correlation_heatmap](https://github.com/user-attachments/assets/feb9d133-d24e-4829-8224-f7a9051169f1)



## Business Insights
  - **Likes and Views:** The high correlation (0.89) between likes and views indicates that as tracks become more popular in terms of views, they are also more likely to receive likes.
  - **Energy and Streams:** A weak correlation (0.04) suggests that energetic tracks do not necessarily lead to higher streaming numbers.
  - **Valence:** The correlation between valence and views, likes, or streams is low, suggesting that a song's emotional positivity (valence) is not a strong driver of engagement.




## Question 2: Identifying Tracks That Need More Promotion (High Engagement, Low Views)
### Goal: To find tracks that have high engagement rates but lower views, indicating that they might benefit from more promotion.
### SQL Query
This query identifies tracks with higher-than-average energy and danceability but moderate views (between the 25th and 75th percentiles) to highlight tracks that could benefit from promotion.
```sql
WITH avg_metrics AS (
    SELECT AVG(energy) AS avg_energy, 
           AVG(danceability) AS avg_danceability
    FROM spotify
),
track_percentiles AS (
    -- Calculate percentiles for views
    SELECT track, views,
           NTILE(100) OVER (ORDER BY views) AS views_percentile
    FROM spotify
)
-- Select tracks in the 25th to 75th percentiles (i.e., moderate engagement)
SELECT s.track, s.artist, s.album, 
       s.energy, s.danceability, s.views, s.likes,
       CASE WHEN s.views > 0 THEN s.likes / s.views ELSE 0 END AS engagement_rate
FROM spotify s
JOIN avg_metrics a ON 1=1  -- Cartesian join to use avg_energy and avg_danceability
JOIN track_percentiles tp ON s.track = tp.track
WHERE s.energy > a.avg_energy
  AND s.danceability > a.avg_danceability
  AND tp.views_percentile BETWEEN 25 AND 75  -- Filter for moderate engagement
ORDER BY s.energy DESC, s.danceability DESC;
```
### Query Results
The results of the SQL query can be found in the spotify_data_2.csv file located in the `data/` folder.
[spotify_data_2.csv](data/spotify_data_2.csv)


### Python Script
This script identifies tracks that have a high engagement rate but relatively low views, indicating that they may benefit from additional promotion. It uses a scatter plot to highlight these tracks.
```python
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load the CSV file
file_path = 'data/spotify_data_2.csv'
df = pd.read_csv(file_path)

# Filter tracks with relevant views
df = df[(df['views'] > 10000) & (df['views'] < 1e8)]  # Focus on tracks between 10k and 100m views

# Calculate engagement rate if not already present
df['engagement_rate'] = df['likes'] / df['views']
df['engagement_rate'] = df['engagement_rate'].fillna(0)

# Replace '#NAME?' with the correct track name 'Equal Sign'
df['track'] = df['track'].replace('#NAME?', 'Equal Sign', regex=False)

# Define thresholds for high engagement and low views
high_engagement_threshold = 0.05  # 5% engagement rate
low_views_threshold = 5e6  # Less than 5 million views

# Highlight tracks with high engagement but low views
df['highlight'] = np.where((df['engagement_rate'] > high_engagement_threshold) & (df['views'] < low_views_threshold), 'Highlight', 'Normal')

# Define bubble size based on engagement rate (but keep it relatively simple)
df['bubble_size'] = df['engagement_rate'] * 500  # Scale bubbles based on engagement, reduced size for simplicity

# Only label the top track for an ultra-simplified view
top_tracks = df[df['highlight'] == 'Highlight'].sort_values(by='engagement_rate', ascending=False).head(1)

# Plot the scatter plot
plt.figure(figsize=(10, 6))
scatter = plt.scatter(df['views'], df['engagement_rate'],
                      s=df['bubble_size'], alpha=0.4,  # Increased transparency
                      c=np.where(df['highlight'] == 'Highlight', 'red', 'blue'))  # Red for highlighted, blue for others

# Add a label only for the top track for simplicity
for i in range(len(top_tracks)):
    plt.text(top_tracks['views'].iloc[i] * 1.05, top_tracks['engagement_rate'].iloc[i], top_tracks['track'].iloc[i],
             fontsize=9, color='black', weight='bold')

# Add horizontal and vertical lines to indicate engagement and views thresholds
plt.axhline(y=high_engagement_threshold, color='green', linestyle='--', label=f'{high_engagement_threshold*100}% Engagement Threshold')
plt.axvline(x=low_views_threshold, color='purple', linestyle='--', label=f'{low_views_threshold/1e6}M Views Threshold')

# Use a logarithmic scale for the x-axis (views)
plt.xscale('log')

# Titles and labels
plt.title('Simplified High-Engagement Tracks Needing Promotion', fontsize=12)
plt.xlabel('Views (Log Scale)', fontsize=10)
plt.ylabel('Engagement Rate (Likes/Views)', fontsize=10)

# Add a legend for the thresholds
plt.legend(fontsize=8)

# Remove or simplify the grid for a cleaner look
plt.grid(False)

# Show plot
plt.show()
```
[promotion_insights.py](scripts/promotion_insights.py)


## Visualization
![high_engagement_tracks_promotion](https://github.com/user-attachments/assets/605b512e-5afc-426e-8a93-0fde66f9d54e)


## Business Insights

  - **High Engagement, Low Views:** Tracks like Safety Zone and Bad Decisions (with BTS & Snoop Dogg) exhibit a high engagement rate but relatively low views. These tracks could benefit from more promotion to increase their visibility.
  - **Potential for Growth:** Promoting these tracks further on streaming platforms could help maximize their reach and improve streaming numbers.




## Question 3: Best Performing Platform by Artist (YouTube vs Spotify)
### Goal: To compare the performance of the top artists on YouTube and Spotify in terms of streams and visualize this comparison using a grouped bar chart.

### SQL Query
This query aggregates the total streams on YouTube and Spotify for each artist and ranks the top 50 artists by total streams.
```sql
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
           SUM(CASE WHEN most_played_on = 'Spotify' THEN comments END) AS spotify_comments
    FROM spotify
    JOIN artist_ranking ON spotify.artist = artist_ranking.artist
    GROUP BY artist_ranking.artist
)
SELECT artist, youtube_streams, spotify_streams, youtube_likes, spotify_likes, youtube_comments, spotify_comments
FROM platform_performance
ORDER BY spotify_streams DESC, youtube_streams DESC;
```

### Query Result
The result is available in the spotify_data_3.csv located in the `data/` folder.
[spotify_data_3.csv](data/spotify_data_3.csv)


### Python Script
This script compares the performance of the top artists on YouTube and Spotify in terms of streams. It generates a grouped bar chart that visualizes the streams on both platforms for the top 10 artists.
```python
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FuncFormatter

# Load the dataset
file_path = 'data/spotify_data_3.csv'
df = pd.read_csv(file_path)

# Filter out rows where streams are null for either platform
df = df.dropna(subset=['youtube_streams', 'spotify_streams'])

# Sort by total streams (Spotify + YouTube) for better visualization
df = df.sort_values(by=['spotify_streams', 'youtube_streams'], ascending=False).head(10)  # Focus on top 10 artists

# Function to format numbers in millions and billions
def format_number(n, pos=None):  # 'pos' is required for FuncFormatter, though it's unused here
    if n >= 1e9:
        return f'{n / 1e9:.2f}B'
    elif n >= 1e6:
        return f'{n / 1e6:.2f}M'
    else:
        return str(n)

# Set the width of the bars
bar_width = 0.35

# Create positions for the bars
r1 = np.arange(len(df['artist']))
r2 = [x + bar_width for x in r1]

# Plotting the bars for YouTube and Spotify streams
plt.figure(figsize=(10, 6))
bars1 = plt.bar(r1, df['youtube_streams'], color='red', width=bar_width, edgecolor='grey', label='YouTube Streams')
bars2 = plt.bar(r2, df['spotify_streams'], color='blue', width=bar_width, edgecolor='grey', label='Spotify Streams')

# Adding the labels
plt.xlabel('Artist', fontsize=12)
plt.ylabel('Streams', fontsize=12)
plt.title('YouTube vs Spotify: Best Performing Platform by Artist', fontsize=14)

# Add xticks on the middle of the group bars
plt.xticks([r + bar_width / 2 for r in range(len(df['artist']))], df['artist'], rotation=45, ha='right')

# Add a legend
plt.legend()

# Apply number formatting to the y-axis
plt.gca().yaxis.set_major_formatter(FuncFormatter(format_number))

# Adjust layout for better label spacing
plt.tight_layout()

# Show the plot
plt.show()
```
[platform_comparison.py](scripts/platform_comparison.py)


### Visualization
![youtube_vs_spotify_streams](https://github.com/user-attachments/assets/6084ad44-6829-45dd-ab72-cb943c197f6d)


### Business Insights
  - **Dominance of Spotify:** For most artists in the dataset, Spotify generally outperforms YouTube in terms of streams. This could imply that these artists have a larger fanbase on Spotify or that Spotify users engage more with their music.
  - **Opportunities for Growth on YouTube:** Some artists, like Dua Lipa, show a strong YouTube presence, which may imply untapped potential on that platform for others.
  - **Artist-Specific Platform Strategy:** Certain artists may benefit from tailored strategies. For example, The Weeknd could explore more YouTube-centric promotions, while Shawn Mendes might focus more on maximizing Spotify streams.

---


## Query Optimization Techniques

### Optimization Techniques Used
- **Indexing**: Indexes on columns like `views`, `artist`, and `likes` to improve query performance.
- **Filtered WHERE Clauses**: Filters like `views > 10,000` and `views < 100,000,000` were applied early to reduce the amount of data processed.
- **Selective Column Retrieval**: Only the relevant columns were selected (e.g., `energy`, `views`, `likes`) to minimize memory usage and increase query speed.
- **Window Functions**: Used `NTILE()` to efficiently calculate the percentiles of tracks without subqueries.
- **Efficient Aggregation**: Aggregate functions (`AVG`, `SUM`, `COUNT`) were used where necessary to summarize data quickly and efficiently.



## Contributing
If you would like to contribute to this project, feel free to fork the repository, submit pull requests, or raise issues.

## License
This project is licensed under the MIT License.

