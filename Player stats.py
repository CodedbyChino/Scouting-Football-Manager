import pandas as pd
import glob
import os
from bs4 import BeautifulSoup

# Function to read and parse HTML file
def read_html_file(file_path):
    with open(file_path, encoding="utf-8") as file:
        soup = BeautifulSoup(file, 'html.parser')
        table = soup.find('table')
        return pd.read_html(str(table), header=0, encoding="utf-8", keep_default_na=True)[0]

# Find the most recent files in the specified folders
first_directory = r'F:\Sports Interactive\Football Manager 2024\shortview\player'
second_directory = r'F:\Sports Interactive\Football Manager 2024\shortview\player2'

# Retrieve file lists
first_list_of_files = glob.glob(os.path.join(first_directory, '*'))
second_list_of_files = glob.glob(os.path.join(second_directory, '*'))

# Error handling for empty directories
if not first_list_of_files:
    raise FileNotFoundError(f"No files found in first directory: {first_directory}")
if not second_list_of_files:
    raise FileNotFoundError(f"No files found in second directory: {second_directory}")

# Find the most recent files
first_latest_file = max(first_list_of_files, key=os.path.getctime)
second_latest_file = max(second_list_of_files, key=os.path.getctime)

# Read HTML files
squad_data_first = read_html_file(first_latest_file)
squad_data_second = read_html_file(second_latest_file)

# Combine data from both files (assuming they have the same structure)
squad_rawdata = pd.concat([squad_data_first, squad_data_second], ignore_index=True)

# Define the columns for technical, mental, and physical attributes
technical_attributes = ["Dri", "Fin", "Fir", "Fre", "Lon", "Pas", "Pen", "Tec"]
mental_attributes = ["Agg", "Ant", "Cmp", "Cnt", "Dec", "Det", "Fla", "Ldr", "OtB", "Pos", "Tea", "Vis", "Wor"]
physical_attributes = ["Acc", "Agi", "Bal", "Jum", "Nat", "Pac", "Sta", "Str"]
personality_weights = {
    "Ambitious": {"Ambition": 18, "Loyalty": 8, "Determination": 17, "Professionalism": 17, "Leadership": 18},
    "Balanced": {},
    "Born Leader": {"Leadership": 20, "Determination": 20},
    "Casual": {"Determination": 5, "Professionalism": 3, "Leadership": 10, "Temperament": 5},
    "Charismatic Leader": {"Leadership": 19.5, "Temperament": 19, "Sportsmanship": 19},
    "Determined": {"Determination": 19, "Ambition": 11, "Professionalism": 17, "Leadership": 18},
    "Devoted": {"Ambition": 6.5, "Loyalty": 20, "Determination": 11.5, "Professionalism": 17, "Leadership": 18},
    "Driven": {"Determination": 19, "Ambition": 16},
    "Easily Discouraged": {"Determination": 1, "Ambition": 5},
    "Fairly Ambitious": {"Ambition": 17.5, "Loyalty": 15, "Professionalism": 17, "Leadership": 18},
    "Fairly Determined": {"Determination": 16, "Professionalism": 14, "Leadership": 18},
    "Fairly Loyal": {"Loyalty": 17.5, "Ambition": 11, "Determination": 10.5, "Professionalism": 17, "Leadership": 18},
    "Fairly Professional": {"Professionalism": 16, "Temperament": 15.5},
    "Fairly Sporting": {"Sportsmanship": 17.5, "Determination": 12, "Ambition": 7.5, "Professionalism": 14},
    "Fickle": {"Loyalty": 5, "Ambition": 18, "Determination": 16, "Professionalism": 17, "Leadership": 18},
    "Honest": {"Sportsmanship": 20, "Determination": 5, "Professionalism": 17, "Leadership": 18},
    "Iron Willed": {"Pressure": 20, "Determination": 16, "Professionalism": 17, "Leadership": 18},
    "Jovial": {"Pressure": 17.5, "Determination": 9, "Professionalism": 17, "Leadership": 18},
    "Leader": {"Leadership": 19.5},
    "Light Hearted": {"Pressure": 17.5, "Sportsmanship": 17.5, "Determination": 17, "Professionalism": 17, "Leadership": 18},
    "Low Determination": {"Determination": 3, "Professionalism": 17, "Leadership": 18},
    "Low Self Belief": {"Professionalism": 2.5, "Determination": 5, "Leadership": 18},
    "Loyal": {"Loyalty": 18.5, "Ambition": 6.5, "Determination": 17, "Professionalism": 17, "Leadership": 18},
    "Mercenary": {"Loyalty": 2, "Ambition": 18, "Determination": 17, "Professionalism": 17, "Leadership": 18},
    "Model Citizen": {"Determination": 17, "Professionalism": 17.5, "Ambition": 16, "Loyalty": 17.5, "Pressure": 17, "Sportsmanship": 17.5, "Temperament": 17.5},
    "Model Professional": {"Professionalism": 20, "Temperament": 15},
    "Perfectionist": {"Determination": 17, "Professionalism": 17, "Ambition": 17},
    "Professional": {"Professionalism": 18.5, "Temperament": 15, "Leadership": 18},
    "Realist": {"Sportsmanship": 3.5, "Determination": 14, "Professionalism": 17, "Leadership": 18},
    "Resilient": {"Pressure": 18, "Determination": 16, "Professionalism": 17, "Leadership": 18},
    "Resolute": {"Determination": 16, "Professionalism": 16, "Leadership": 18},
    "Slack": {"Professionalism": 1, "Determination": 5, "Temperament": 5, "Leadership": 18},
    "Spineless": {"Pressure": 1, "Determination": 5, "Leadership": 18},
    "Spirited": {"Pressure": 17.5, "Professionalism": 14, "Determination": 17, "Leadership": 18},
    "Sporting": {"Sportsmanship": 18.5, "Determination": 5, "Professionalism": 17, "Leadership": 18},
    "Temperamental": {"Temperament": 2.5, "Professionalism": 5.5},
    "Unambitious": {"Ambition": 3, "Loyalty": 15.5, "Determination": 17, "Professionalism": 17, "Leadership": 18},
    "Unsporting": {"Sportsmanship": 1, "Determination": 14, "Professionalism": 17, "Leadership": 18},
    "Very Ambitious": {"Ambition": 20, "Loyalty": 8, "Determination": 17, "Professionalism": 17, "Leadership": 18},
    "Very Loyal": {"Loyalty": 20, "Ambition": 6.5, "Determination": 17, "Professionalism": 17, "Leadership": 18},
}

# Calculate the mean for each personality type
personality_scores = {}
for personality_type, attributes in personality_weights.items():
    if attributes:
        mean_value = sum(attributes.values()) / len(attributes)
        personality_scores[personality_type] = mean_value
    else:
        personality_scores[personality_type] = 0

# Check if the attribute columns exist in the DataFrame
missing_columns = set(technical_attributes + mental_attributes + physical_attributes) - set(squad_rawdata.columns)
if missing_columns:
    raise ValueError(f"Columns {missing_columns} are missing in the DataFrame.")

# Convert attribute columns to numeric
squad_rawdata[technical_attributes + mental_attributes + physical_attributes] = squad_rawdata[technical_attributes + mental_attributes + physical_attributes].apply(pd.to_numeric, errors='coerce')

# Calculate average ability for each player in different categories
squad_rawdata['technical_ability'] = squad_rawdata[technical_attributes].mean(axis=1).round(1)
squad_rawdata['physical_ability'] = squad_rawdata[physical_attributes].mean(axis=1).round(1)
squad_rawdata['mental_ability'] = squad_rawdata[mental_attributes].mean(axis=1).round(1)
squad_rawdata['personality_scores'] = squad_rawdata['Personality'].map(personality_scores)

squad_rawdata['overall_ability'] = squad_rawdata[
    ['technical_ability', 'physical_ability', 'mental_ability', 'personality_scores']
].mean(axis=1)

# Output the results
for index, player in squad_rawdata.iterrows():
    print(f"Player: {player['Name']} ({player['Age']})")
    print(f"Technical Average: {player['technical_ability']:.2f}")
    print(f"Mental Average: {player['mental_ability']:.2f}")
    print(f"Physical Average: {player['physical_ability']:.2f}")
    
    personality = player.get('Personality', None)
    if personality is not None:
        personality_score = personality_scores.get(personality, None)
        if personality_score is not None:
            print(f"Personality: {personality} - Score: {personality_score:.2f}")
  
    print(f"Overall Average: {player['overall_ability']:.2f}")
    print("-" * 20)
