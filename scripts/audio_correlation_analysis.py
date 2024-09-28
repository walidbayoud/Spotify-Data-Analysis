import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the CSV file
file_path = '/Users/Admin/Downloads/spotify_data_1.csv'
df = pd.read_csv(file_path)

# Select relevant columns for correlation analysis
columns_to_analyze = ['energy', 'danceability', 'tempo', 'valence', 'views', 'likes', 'stream']
df_corr = df[columns_to_analyze]

# Calculate the correlation matrix
correlation_matrix = df_corr.corr()

# Define Spotify theme colors
spotify_green = '#1DB954'
spotify_black = '#191414'
spotify_white = '#FFFFFF'

# Set consistent font and grid styles for the entire project
plt.rcParams.update({'font.size': 12, 'font.family': 'Arial', 'grid.color': spotify_black, 'grid.linestyle': '--'})

# Create the heatmap for correlations with Spotify colors
plt.figure(figsize=(10, 8))
sns.set_theme(style="whitegrid")
sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", linewidths=0.5, linecolor=spotify_black, annot_kws={"size": 10, "color": spotify_black})

# Add title and format
plt.title('Correlation Between Audio Features and Engagement Metrics', fontsize=14, color=spotify_black)
plt.xticks(fontsize=12, color=spotify_black)
plt.yticks(fontsize=12, color=spotify_black)
plt.show()
