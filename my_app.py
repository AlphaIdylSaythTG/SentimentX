import streamlit as st
from textblob import TextBlob
import altair as alt
import pandas as pd
from PIL import Image
import numpy as np
import base64

# Function to download CSV file
def download_csv(df):
    
    # Convert the DataFrame to a CSV file
    csv = df.to_csv(index=False)
    
    # Encode the CSV file as base64
    b64 = base64.b64encode(csv.encode()).decode()
    
    # Create a download link for the CSV file
    href = f'<a href="data:file/csv;base64,{b64}" download="sentiment_log.csv">Download CSV file</a>'
    
    return href

def predict_sentiment(text):
    blob = TextBlob(text)
    sentiment_score = blob.sentiment.polarity
    return sentiment_score

def get_sentiment_message(sentiment_score):
    if sentiment_score > 0.5:
        return 'Very Positive'
    elif sentiment_score > 0:
        return 'Positive'
    elif sentiment_score == 0:
        return 'Neutral'
    elif sentiment_score < -0.5:
        return 'Very Negative'
    else:
        return 'Negative'

def predict_image_sentiment(image_file):
    sentiment_score = 0.5 #Needs to get implemented
    return sentiment_score

def main():
    st.set_page_config(page_title="SentimentX", page_icon=":heart:", layout="wide")

    # Create a menu with four options: Predict Sentiment, Sentiment Log, EmoVision
    menu = ['EmoText', 'Logs', 'EmoVision']
    choice = st.sidebar.selectbox('Select an option', menu)

    # If the user selects 'Predict Sentiment'
    if choice == 'EmoText':
        st.title('EmoText!')
        st.write('Enter some text and the app will predict its sentiment')

        # Initialize the session state
        if 'user_input' not in st.session_state:
            st.session_state.user_input = []
            st.session_state.sentiment_scores = []

        user_input = st.text_input("Enter your text here")

        if st.button('Predict Sentiment'):
            sentiment_score = predict_sentiment(user_input)
            sentiment_message = get_sentiment_message(sentiment_score)
    
            # Store the user input and sentiment score in the session state
            st.session_state.user_input.append(user_input)
            st.session_state.sentiment_scores.append(sentiment_score)

            st.write('The sentiment score is:', sentiment_score)
            
            st.write('The sentiment is:', sentiment_message)

        # Create a sentiment analysis graph
        data = pd.DataFrame({'time': range(len(st.session_state.sentiment_scores)), 'score': st.session_state.sentiment_scores})
        chart = alt.Chart(data).mark_line().encode(
            x='time',
            y='score',
            tooltip=['time', 'score']
        ).properties(
            width=600,
            height=400
        ).configure_axis(
            labelFontSize=14,
            titleFontSize=16
        ).configure_title(
            fontSize=20
        )
        st.altair_chart(chart, use_container_width=True)

    # If the user selects 'Sentiment Log'
    elif choice == 'Logs':
        st.title('Logs')

        # If no sentiment scores have been recorded yet, display a message
        if not st.session_state.sentiment_scores:
            st.write('No sentiment scores recorded yet')
        else:
            # Display a table of the user inputs and sentiment scores
            # Call get_sentiment_message() for each sentiment score and create a list of sentiment messages
            sentiment_messages = [get_sentiment_message(score) for score in st.session_state.sentiment_scores]

            data = pd.DataFrame({'Input': st.session_state.user_input, 'Score': st.session_state.sentiment_scores, 'Rating': sentiment_messages})
            st.write(data)

            # Allow the user to download the sentiment log as a CSV file
            st.markdown(download_csv(data), unsafe_allow_html=True)

    # If the user selects 'EmoVision'
    elif choice == 'EmoVision':
        st.title('EmoVision')
        st.write('Upload an image and the app will perform sentiment analysis on it')

        # Create a file uploader for images
        uploaded_file = st.file_uploader("Choose an image file", type=['jpg', 'jpeg', 'png'])

        if uploaded_file is not None:
            # Display the uploaded image
            st.image(uploaded_file, caption='Uploaded Image', use_column_width=True)
            
            # Perform sentiment analysis on the image
            sentiment_score =  predict_image_sentiment(uploaded_file)#0.5 # Replace with actual sentiment analysis code

            sentiment_message = get_sentiment_message(sentiment_score)

            # Store the image and sentiment analysis results in the session state
            st.session_state.sentiment_score = sentiment_score
            st.session_state.sentiment_message = sentiment_message

            # Display the sentiment analysis results
            st.write('The sentiment score is:', sentiment_score)
            st.write('The sentiment is:', sentiment_message)

     

    # Add a footer to the app
    st.sidebar.markdown("---")
    st.write("Created by Yash Thapliyal 2023")
if __name__ == '__main__':
    main()
