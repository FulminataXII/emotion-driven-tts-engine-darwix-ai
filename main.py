from fastapi import FastAPI, HTTPException
from fastapi.responses import Response
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from fastapi.responses import FileResponse

# Import your existing scripts
from emotion_classifier import setup_classifier, predict_emotion
from tts_part import synthesize_speech

app = FastAPI()

# # Mount the 'static' directory to serve our HTML/CSS/JS
# app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize the classifier model once when the server starts
print("Initializing backend models...")
classifier_model = setup_classifier()

class TextInput(BaseModel):
    text: str

@app.get("/")
async def index_page():
    return FileResponse("static/index.html")

@app.post("/generate-audio")
async def generate_audio(input_data: TextInput):
    if not input_data.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty.")
    
    try:
        # 1. Predict Emotion
        emotion, confidence = predict_emotion(classifier_model, input_data.text)
        print(f"Detected Emotion: [{emotion.upper()}] (Confidence: {confidence:.2f})")
        
        # 2. Synthesize Speech (Hardcoded to male voice)
        audio_bytes = synthesize_speech(text=input_data.text, emotion=emotion, gender="male")
        
        # 3. Return the MP3 file directly to the browser
        return Response(content=audio_bytes, media_type="audio/mpeg")
        
    except Exception as e:
        print(f"Error generating audio: {e}")
        raise HTTPException(status_code=500, detail="Internal server error during audio generation.")


















# # Import the functions from your two modules
# from emotion_classifier import setup_classifier, predict_emotion
# from tts_prototype import synthesize_speech

# def run_pipeline():
#     print("=== Emotion-Driven TTS Pipeline ===")
    
#     # 1. Initialize the Hugging Face model once at startup
#     # This prevents the pipeline from reloading the heavy model for every single sentence
#     print("Initializing components...")
#     classifier_model = setup_classifier()
    
#     # Select the voice gender for the session
#     gender = input("Select voice gender ('female' or 'male') [default: female]: ").strip().lower()
#     if gender not in ['female', 'male']:
#         gender = 'female'

#     print("\nPipeline Ready! Type 'exit' or 'quit' to stop.")
#     print("-" * 35)

#     # 2. Interactive Loop
#     while True:
#         # Get text input from the user
#         user_text = input("\nEnter text to synthesize: ").strip()
        
#         # Exit condition
#         if user_text.lower() in ['exit', 'quit']:
#             print("Exiting pipeline. Goodbye!")
#             break
            
#         if not user_text:
#             continue

#         try:
#             # Step A: Classify the text
#             print("Classifying emotion...")
#             emotion, confidence = predict_emotion(classifier_model, user_text)
#             print(f"-> Detected Emotion: [{emotion.upper()}] (Confidence: {confidence:.1%})")

#             # Step B: Synthesize the speech
#             print("Generating audio...")
#             # We pass the text, the detected emotion, and the chosen gender to the TTS engine
#             synthesize_speech(text=user_text, emotion=emotion, gender=gender)
            
#         except Exception as e:
#             print(f"An error occurred during processing: {e}")

# if __name__ == "__main__":
#     run_pipeline()