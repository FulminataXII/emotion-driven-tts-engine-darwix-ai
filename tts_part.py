import json
import re
from google.cloud import texttospeech

def load_emotion_config(filepath="config.json"):
    """Loads the SSML parameters from the JSON file."""
    with open(filepath, "r") as file:
        return json.load(file)

def generate_ssml(text, emotion, config):
    """Wraps text in SSML tags based on the emotion configuration."""
    params = config.get(emotion, config["neutrality"])
    
    # Split text into sentences to insert appropriate breaks
    sentences = [s.strip() for s in re.split(r'(?<=[.!?]) +', text) if s.strip()]
    
    break_tag = f'<break time="{params["break_time"]}"/>'
    
    text_with_breaks = f" {break_tag} ".join(sentences)
    
    # Wrap everything in the prosody tag
    ssml = (
        f"<speak>"
        f'<prosody pitch="{params["pitch"]}" '
        f'volume="{params["volume"]}" '
        f'rate="{params["rate"]}">'
        f'{text_with_breaks}'
        f'</prosody>'
        f"</speak>"
    )
    return ssml

async def synthesize_speech(text, emotion, gender="female"):
    """Generates audio from text and saves it as an MP3."""
    config = load_emotion_config()

    if gender not in ["female", "male"]:
        print(f"Warning: Gender '{gender}' not recognized. Defaulting to 'female'.")
        gender = "female"
        
    gender_config = config[gender]
    
    if emotion not in gender_config:
        print(f"Emotion '{emotion}' not found in config. Defaulting to neutrality.")
        emotion = "neutrality"

    ssml = generate_ssml(text, emotion, gender_config)
    print(f"Generated SSML:\n{ssml}\n")

    client = texttospeech.TextToSpeechAsyncClient()

    synthesis_input = texttospeech.SynthesisInput(ssml=ssml)

    voice_name = "en-US-Neural2-F" if gender == "female" else "en-US-Neural2-D"

    
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name=voice_name 
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = await client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    return response.audio_content


# --- Testing ---
if __name__ == "__main__":
    sample_text_joy = "I'm so happy right now about my recent lifestyle changes. "
    sample_text_sad = "I can't believe this is happening. Everything's falling apart. I feel terrible. "
    sample_text_anger = "Why the fuck would you not listen to me? I've given the simplest instructions a monkey could follow, which apparantly aren't simple enough for you!"
    sample_text_fear = "I can't believe this is happening. What do I do now?"
    sample_text_disgust = "Eww!! What's that smell??"
    sample_text_surprise = "Woww!!"
    sample_text_neutral = "Who cares? I certainly don't. "
    
    response = synthesize_speech(sample_text_anger, "anger", "male")

    output_filename = f"output.mp3"
    with open(output_filename, "wb") as out:
        out.write(response)
        print(f"Audio content written to file: {output_filename}")