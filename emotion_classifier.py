from transformers import pipeline

def setup_classifier():
    """
    Downloads and initializes the emotion classification model.
    This will take a moment the first time you run it as it downloads the model weights (~260MB).
    """
    print("Loading Hugging Face model (michelleli99/emotion_text_classifier)...")
    
    # Initialize the text-classification pipeline
    classifier = pipeline(
        task="text-classification", 
        model="michelleli99/emotion_text_classifier",
        # Set to True if you want to see the probabilities for all 7 emotions
        # Set to False to just get the top predicted emotion
        top_k=1 
    )
    print("Model loaded successfully!\n")
    return classifier

def predict_emotion(classifier, text):
    """
    Passes the text to the model and extracts the predicted emotion.
    """
    results = classifier(text)
    
    top_prediction = results[0][0]
    emotion = top_prediction['label']
    confidence = top_prediction['score']
    
    return emotion, confidence

# --- Testing ---
if __name__ == "__main__":
    emotion_model = setup_classifier()
    
    test_sentences = [
        "I cannot believe this is happening. We need to do something about it right now!",
        "I just got the job offer! This is the best day of my life!",
        "I'm feeling really drained and empty today. Nothing seems to matter.",
        "Eww, there is mold growing all over this bread.",
        "The package will arrive on Tuesday between 9 AM and 5 PM."
    ]
    
    for sentence in test_sentences:
        emotion, confidence = predict_emotion(emotion_model, sentence)
        
        print(f"Text: '{sentence}'")
        print(f"Predicted Emotion: [{emotion}] (Confidence: {confidence:.1%})\n")