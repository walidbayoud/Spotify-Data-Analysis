import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FuncFormatter

# Load the dataset
file_path = '/Users/Admin/Downloads/spotify_platform_comparison.csv'
df = pd.read_csv(file_path)

# Filter out rows where streams are null for either platform
df = df.dropna(subset=['youtube_streams', 'spotify_streams'])

# Sort by total streams (Spotify + YouTube)
df = df.sort_values(by=['spotify_streams', 'youtube_streams'], ascending=False).head(10)

# Function to format numbers in millions and billions
def format_number(n, pos=None):
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

# Define Spotify-themed colors
spotify_green = '#1DB954'
youtube_red = '#FF6347'
spotify_black = '#191414'

# Set consistent font and grid styles for the entire project
plt.rcParams.update({'font.size': 12, 'font.family': 'Arial', 'grid.color': spotify_black, 'grid.linestyle': '--'})

# Plotting the bars for YouTube and Spotify streams
plt.figure(figsize=(10, 6))
bars1 = plt.bar(r1, df['youtube_streams'], color=youtube_red, width=bar_width, edgecolor='grey', label='YouTube Streams')
bars2 = plt.bar(r2, df['spotify_streams'], color=spotify_green, width=bar_width, edgecolor='grey', label='Spotify Streams')

# Adding the labels
plt.xlabel('Artist', fontsize=12, color=spotify_black)
plt.ylabel('Streams', fontsize=12, color=spotify_black)
plt.title('YouTube vs Spotify: Best Performing Platform by Artist', fontsize=14, color=spotify_black)

# Add xticks on the middle of the group bars
plt.xticks([r + bar_width / 2 for r in range(len(df['artist']))], df['artist'], rotation=45, ha='right', fontsize=10, color=spotify_black)

# Add a legend
plt.legend(fontsize=10)

# Apply number formatting to the y-axis
plt.gca().yaxis.set_major_formatter(FuncFormatter(format_number))
plt.yticks(fontsize=10, color=spotify_black)

# Show plot
plt.show()
