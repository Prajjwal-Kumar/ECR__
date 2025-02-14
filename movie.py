import random
import pandas as pd
import nltk
from textblob import TextBlob
from nltk.sentiment import SentimentIntensityAnalyzer

# Download VADER lexicon if not already present
nltk.download('vader_lexicon')
sia = SentimentIntensityAnalyzer()

# Load the dataset from the Excel file
file_path = "bollywood_movie_dataset.xlsx"
movies_df = pd.read_excel(file_path)

# List of possible emotions
EMOTIONS = {
    "Happy": ["joy", "excited", "pleased", "cheerful", "delighted", "content", "thrilled"],
    "Sadness": ["down", "unhappy", "heartbroken", "depressed", "miserable", "lonely", "cry", "low", "blue"],
    "Motivational": ["motivated", "success", "inspired", "determined", "achieve", "goal", "strong"],
    "Thrilling": ["excited", "adrenaline", "tense", "shocking", "suspense", "nerve-wracking"],
    "Romantic": ["love", "romance", "affection", "passionate", "crush", "heartfelt"],
    "Mind-Bending": ["confused", "philosophical", "thought-provoking", "mind-blowing", "trippy"],
    "Excited": ["thrilled", "energetic", "enthusiastic", "hyped", "elated"],
    "Angry": ["furious", "mad", "revengeful", "annoyed", "irritated", "rage", "pissed"],
    "Relaxed": ["calm", "peaceful", "chill", "serene", "soothing"],
    "Nostalgic": ["memories", "past", "sentimental", "childhood", "old times"],
    "Fearful": ["scared", "horror", "frightened", "terrified", "panic", "uneasy"],
    "Surprised": ["shocked", "unexpected", "twist", "astonished", "amazed"],
    "Inspired": ["dream", "aspiration", "hopeful", "vision", "uplifted"]
}

def detect_emotion(text):
    sentiment_score = sia.polarity_scores(text)["compound"]
    words = text.lower().split()
    detected_emotions = []
    
    for emotion, keywords in EMOTIONS.items():
        if any(keyword in words for keyword in keywords):
            detected_emotions.append(emotion)
    
    if detected_emotions:
        return detected_emotions[0]
    
    if sentiment_score >= 0.4:
        return "Happy"
    elif sentiment_score <= -0.2:
        return "Sadness"
    
    return "Neutral"

def recommend_movie(emotion):
    if emotion in ["Sadness", "Angry", "Fearful"]:
        emotion = "Happy"
    
    filtered_movies = movies_df[movies_df["Emotion"].str.lower() == emotion.lower()]
    if not filtered_movies.empty:
        recommendations = filtered_movies.sample(n=min(3, len(filtered_movies)), replace=False, random_state=random.randint(1, 10000))
        return recommendations[["Movie", "Genre"]].drop_duplicates().to_dict(orient="records")
    return []

def chatbot():
    print("Hello! Tell me how you're feeling, and I'll recommend a Bollywood movie for you.")
    print(f"Possible emotions: {', '.join(EMOTIONS.keys())}")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit", "bye"]:
            print("Chatbot: Goodbye! Enjoy your movie!")
            break
        emotion = detect_emotion(user_input)
        recommendations = recommend_movie(emotion)
        
        if recommendations:
            if emotion in ["Sadness", "Angry", "Fearful"]:
                response = (
                    f"I understand that you're feeling {emotion}. It's completely okay to have these emotions. Sometimes, a lighthearted or uplifting movie can make a big difference. "
                    f"Here are some Bollywood movies that might brighten your day: {', '.join([movie['Movie'] for movie in recommendations])}. "
                    f"Take a deep breath, grab some snacks, and enjoy these wonderful stories!"
                )
            else:
                response = (
                    f"I sense that you're feeling {emotion}. Movies can be a great way to match or even elevate your mood. "
                    f"Here are some Bollywood movies that you might enjoy: {', '.join([movie['Movie'] for movie in recommendations])}. "
                    f"Enjoy your time and immerse yourself in these cinematic experiences!"
                )
        else:
            response = "I couldn't find a perfect match, but watching a great movie always helps! Try '3 Idiots' for a fun and inspiring experience. Keep your spirits up!"
        
        print({"emotion": emotion, "recommendations": recommendations, "response": response})

if __name__ == "__main__":
    chatbot()
