import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load the CSV file
file_path = '/Users/Admin/Downloads/spotify_data_2.csv'
df = pd.read_csv(file_path)

# Filter tracks with relevant views
df = df[(df['views'] > 10000) & (df['views'] < 1e8)]  # Focus on tracks between 10k and 100m views

# Calculate engagement rate
df['engagement_rate'] = df['likes'] / df['views']
df['engagement_rate'] = df['engagement_rate'].fillna(0)

# Replace '#NAME?' with the correct track name 'Equal Sign'
df['track'] = df['track'].replace('#NAME?', 'Equal Sign', regex=False)

# Define thresholds for high engagement and low views
high_engagement_threshold = 0.05  # 5% engagement rate
low_views_threshold = 5e6  # Less than 5 million views

# Highlight tracks with high engagement but low views
df['highlight'] = np.where((df['engagement_rate'] > high_engagement_threshold) & (df['views'] < low_views_threshold), 'Highlight', 'Normal')

# Define bubble size based on engagement rate
df['bubble_size'] = df['engagement_rate'] * 500  # Scale bubbles based on engagement

# Only label the top track for an ultra-simplified view
top_tracks = df[df['highlight'] == 'Highlight'].sort_values(by='engagement_rate', ascending=False).head(1)

# Define Spotify-themed colors
spotify_green = '#1DB954'
spotify_black = '#191414'
spotify_purple = '#8A2BE2'

# Set consistent font and grid styles for the entire project
plt.rcParams.update({'font.size': 12, 'font.family': 'Arial', 'grid.color': spotify_black, 'grid.linestyle': '--'})

# Plot the scatter plot
plt.figure(figsize=(10, 6))
scatter = plt.scatter(df['views'], df['engagement_rate'],
                      s=df['bubble_size'], alpha=0.6,  # Consistent transparency
                      c=np.where(df['highlight'] == 'Highlight', spotify_green, spotify_black))  # Red for highlighted, blue for others

# Add a label only for the top track
for i in range(len(top_tracks)):
    plt.text(top_tracks['views'].iloc[i] * 1.05, top_tracks['engagement_rate'].iloc[i], top_tracks['track'].iloc[i],
             fontsize=10, color=spotify_black, weight='bold')

# Add horizontal and vertical lines to indicate engagement and views thresholds
plt.axhline(y=high_engagement_threshold, color=spotify_green, linestyle='--', label=f'{high_engagement_threshold*100}% Engagement Threshold')
plt.axvline(x=low_views_threshold, color=spotify_purple, linestyle='--', label=f'{low_views_threshold/1e6}M Views Threshold')

# Use a logarithmic scale for the x-axis (views)
plt.xscale('log')

# Titles and labels
plt.title('Simplified High-Engagement Tracks Needing Promotion', fontsize=14, color=spotify_black)
plt.xlabel('Views (Log Scale)', fontsize=12, color=spotify_black)
plt.ylabel('Engagement Rate (Likes/Views)', fontsize=12, color=spotify_black)

# Add a legend for the thresholds
plt.legend(fontsize=10)

# Show plot
plt.show()
