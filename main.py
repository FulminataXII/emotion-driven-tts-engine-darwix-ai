from fastapi import FastAPI, HTTPException
from fastapi.responses import Response
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from fastapi.responses import FileResponse
from fastapi.concurrency import run_in_threadpool

from emotion_classifier import setup_classifier, predict_emotion
from tts_part import synthesize_speech

app = FastAPI()


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
        emotion, confidence = await run_in_threadpool(predict_emotion, classifier_model, input_data.text)
        print(f"Detected Emotion: [{emotion.upper()}] (Confidence: {confidence:.2f})")
        
        audio_bytes = await synthesize_speech(text=input_data.text, emotion=emotion, gender="male")
        
        return Response(content=audio_bytes, media_type="audio/mpeg")
        
    except Exception as e:
        print(f"Error generating audio: {e}")
        raise HTTPException(status_code=500, detail="Internal server error during audio generation.")

