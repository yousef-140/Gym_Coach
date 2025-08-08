import pandas as pd
from langchain.schema import Document

def clean_food_data(path):
    df = pd.read_csv(path)
    df = df.dropna().drop_duplicates()
    documents = []

    for _, row in df.iterrows():
        text = (
            f"{row['Food_Item']} is a {row['Category']} item with {row['Calories (kcal)']} kcal, "
            f"{row['Protein (g)']}g protein, {row['Carbohydrates (g)']}g carbs, "
            f"{row['Fat (g)']}g fat, {row['Fiber (g)']}g fiber, and {row['Sugars (g)']}g sugar."
        )
        documents.append(Document(page_content=text, metadata={"source": "food_nutrition"}))
    return documents


def clean_meal_plans(path):
    df = pd.read_csv(path)
    df = df.dropna().drop_duplicates()
    documents = []

    for _, row in df.iterrows():
        text = (
            f"The meal '{row['meal_name']}' contains {row['calories']*1000:.0f} kcal, "
            f"protein score: {row['protein']:.2f}, fat score: {row['fat']:.2f}, "
            f"carb score: {row['carbs']:.2f}, and takes approx {row['prep_time']*100:.0f} minutes to prepare. "
            f"Diet tags — Vegan: {bool(row['vegan'])}, Keto: {bool(row['keto'])}, Gluten-Free: {bool(row['gluten_free'])}."
        )
        documents.append(Document(page_content=text, metadata={"source": "meal_plans"}))
    return documents


def clean_gym_dataset(path):
    df = pd.read_csv(path)
    df = df.dropna(subset=["Title", "Desc", "Type", "BodyPart"])
    df = df.drop_duplicates()
    documents = []

    for _, row in df.iterrows():
        text = (
            f"Exercise: {row['Title']} - {row['Desc']} It targets the {row['BodyPart']} and is a {row['Type']} type exercise. "
            f"Equipment used: {row.get('Equipment', 'N/A')}, suitable for level: {row.get('Level', 'Unknown')}."
        )
        documents.append(Document(page_content=text, metadata={"source": "gym_dataset"}))
    return documents


def clean_exercise_file(path):
    df = pd.read_excel(path)
    df = df.dropna(subset=["Exercise_Name", "Description_URL", "muscle_gp"])
    df = df.drop_duplicates()
    documents = []

    for _, row in df.iterrows():
        text = (
            f"Exercise: {row['Exercise_Name']}, targets: {row['muscle_gp']}. "
            f"More info: {row['Description_URL']}. Images available: {row['Exercise_Image'] or 'None'}"
        )
        documents.append(Document(page_content=text, metadata={"source": "exercise_dataset"}))
    return documents


food_docs = clean_food_data("daily_food_nutrition_dataset.csv")
meal_docs = clean_meal_plans("healthy_meal_plans.csv")
gym_docs = clean_gym_dataset("megaGymDataset.csv")
exercise_docs = clean_exercise_file("Gym Exercises Dataset.xlsx")

# Combine everything
all_clean_documents = food_docs + meal_docs + gym_docs + exercise_docs

import pickle

with open("cleaned_docs.pkl", "wb") as f:
    pickle.dump(all_clean_documents, f)

print(" Saved cleaned documents to cleaned_docs.pkl")
