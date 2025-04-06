import streamlit as st
import pymongo
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import load_model
import pickle
import pandas as pd



# MongoDB connection details
mongo_uri = "mongodb+srv://sentimental_analysis:sentimental_analysis_predction@cluster0.vxky4.mongodb.net/"
client = pymongo.MongoClient(mongo_uri)
db = client["sentiment_analysis_db"]
collection = db["sentiment_results"]

# Load Model & Tokenizer
@st.cache_resource
def load_lstm_model():
    return load_model(r"D:\\Level 6\\Sentiment_Analaysis_Tool\\authentication\\pages\\Sentiment_Analysis_Model.h5")

model = load_lstm_model()

with open(r"D:\\Level 6\\Sentiment_Analaysis_Tool\\authentication\\pages\\Sentiment_Analysis_Model_model.pkl", "rb") as handle:
    tokenizer = pickle.load(handle)

tokenizer = Tokenizer()

def preprocess_text(text, max_length=100):
    sequence = tokenizer.texts_to_sequences([text])  # ✅ Correct: Use tokenizer, not model
    return pad_sequences(sequence, maxlen=max_length)

def predict_sentiment(text):
    padded = preprocess_text(text)
    prediction = model.predict(padded)[0][0]

    # Classify sentiment
    if prediction > 0.6:
        return "Positive", round(prediction, 2)
    elif prediction < 0.4:
        return "Negative", round(prediction, 2)
    else:
        return "Neutral", round(prediction, 2)

# Streamlit UI
st.header('Sentiment Analysis Tool')

# Single Text Analysis
with st.expander('Analyze Text'):
    text = st.text_input('Enter text:')
    if text:
        sentiment, confidence = predict_sentiment(text)
        st.write(f"Predicted Sentiment: {sentiment} (Confidence: {confidence})")

        # Save to MongoDB
        if st.button("Save to Database"):
            result = {
                "text": text,
                "sentiment": sentiment,
                "confidence": confidence,
                "analyzed_at": pd.to_datetime('now')
            }
            collection.insert_one(result)
            st.success("Result saved successfully!")

# CSV File Analysis
with st.expander('Analyze CSV File'):
    uploaded_file = st.file_uploader("Upload a CSV file", type=['csv'])

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)

        if 'text' in df.columns:
            df['Sentiment'], df['Confidence'] = zip(*df['text'].apply(predict_sentiment))
            st.write("Predicted Sentiments:")
            st.dataframe(df)

            # Save all results to MongoDB
            if st.button("Save All to Database"):
                for _, row in df.iterrows():
                    result = {
                        "text": row['text'],
                        "sentiment": row['Sentiment'],
                        "confidence": row['Confidence'],
                        "analyzed_at": pd.to_datetime('now')
                    }
                    collection.insert_one(result)
                st.success("All results saved successfully!")

            # Download results
            output_csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(label="Download Results", data=output_csv, file_name="sentiment_results.csv", mime="text/csv")

        else:
            st.error("Error: CSV must contain a 'text' column!")

# Display Stored Results from MongoDB
with st.expander('View Stored Results'):
    results = list(collection.find().sort("analyzed_at", -1))  # Fetch and sort by analyzed_at

    if results:
        df_results = pd.DataFrame(results)
        df_results = df_results[["text", "sentiment", "confidence", "analyzed_at"]]  # Select relevant columns
        st.dataframe(df_results)
    else:
        st.write("No results found.")
