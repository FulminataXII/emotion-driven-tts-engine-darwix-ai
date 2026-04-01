# Emotion-Driven TTS Pipeline

A lightweight, real-time web application that classifies the emotional tone of input text using a Hugging Face Transformer model and synthesizes expressive audio using Google Cloud's Text-to-Speech API. This sets a precedent for applications where when text with the intended emotion is passed, an expressive speech carrying the intended emotion is generated. This truly makes the automated exchanges with customers much more lively and feel more human. The pipeline uses Google Cloud's TTS API as it is one of the industry standards for using TTS in automated communication adn because the API supports further customization of speech allowing industry specific abbrevatiions and terms to be pronounced correctly through SSML. 

## Tech-Stack
* **Backend:** FastAPI, Python 3.9+
* **ML Pipeline:** Hugging Face `transformers`, PyTorch (using `michelleli99/emotion_text_classifier`)
* **TTS Engine:** Google Cloud Text-to-Speech 
* **Frontend:** HTML/CSS/JS 

# How to run the pipeline? 
Follow the steps below to run it. 
## Prerequisites
1. **Google Cloud Account:** You must have an active GCP project with the **Cloud Text-to-Speech API** enabled.
2. **Service Account Key:** A JSON key with permissions to call the TTS API.  
*Follow [Step 3](#3-configure-credentials) in Local Setup if GCP Project and Service account Key aren't setup already.*
3. **Python 3.9+** installed locally.

## Local Setup

### 1. Clone the Repo
Clone the repository and initialize a virtual environment:

```bash
git clone <your-repo-url>
cd <your-repo-folder>

python -m venv venv
# On macOS/Linux:
source venv/bin/activate  
# On Windows: 
venv\Scripts\activate
```

Ensure that the project directory is as follows:

```text
.
├── main.py                  # FastAPI application
├── emotion_classifier.py    # HF pipeline initialization
├── tts_part.py              # GCP TTS client and SSML generation
├── config.json              # Contains the prosody changes for each emotion
└── static/
    └── index.html           # Minimal frontend UI
```

### 2. Install Dependencies
Install the required packages. 

```bash
pip install fastapi uvicorn transformers torch google-cloud-texttospeech pydantic
```

### 3. Configure Credentials
#### I.   Create a new Project on Google Cloud. 
#### II.  Enable 'Google Cloud Text-to-Speech API' service. 
#### III. Go to IAM & Admin > Service Accounts.
#### IV.  Click Create Service Account and give it a name. 
#### V.   Click on your newly created service account and go to the Keys tab > Add Key > Create new key > JSON.
Save this file securely on your machine (e.g., credentials.json).

#### VI. Add the path to the local environment. 
*Note: This command should be run everytime a new terminal is opened to run the app.*

**Linux/macOS:**
```bash
export GOOGLE_APPLICATION_CREDENTIALS="/absolute/path/to/your/credentials.json"
```

**Windows (Command Prompt):**
```cmd
set GOOGLE_APPLICATION_CREDENTIALS="C:\absolute\path\to\your\credentials.json"
```

**Windows (PowerShell):**
```powershell
$env:GOOGLE_APPLICATION_CREDENTIALS="C:\absolute\path\to\your\credentials.json"
```

## Running the Server

Start the FastAPI application via Uvicorn:

```bash/cmd/powershell
uvicorn main:app --reload
```
*The initial startup will take a few moments as it downloads the ~260MB Hugging Face model weights into memory.*

Once the server is running, access the web interface at:
**http://localhost:8000/**



## How It Works

### emotion_classifier.py
This file contains the part of the pipeline that takes a string of text as input and uses michelleli99's [emotion_text_classifier](https://huggingface.co/michelleli99/emotion_text_classifier) transformer model to classify it into 7 distinct class of emotions: anger, disgust, fear/panic, joy, neutrality, sadness, and surprise. 

### tts_part.py
This file contains the code which takes a string of text along with the intended emotion to be spoken in. It uses SSML to encode the changes in three distinct prosodical elements: pitch, loudness/volume, and rate. The choice of the values for these prosodical elements to reflect the emotion is made following extensive research done by [Rainer Banse & Klaus R. Scherer](https://www.researchgate.net/publication/14353171_Acoustic_Profiles_in_Vocal_Emotion_Expression). The following are the direct conclusions made from the reasearch paper:  
#### 1. Anger
Anger, here, is referred to as "hot anger" in the paper and is associated with increase in mean F0 (pitch) and rate of articulation. 
#### 2. Disgust
Disgust is associated with decrease in mean F0 (pitch), with a decrease in rate and increase in volume, although very minimal.
#### 3. Fear
Fear, here, is referred to as "panic" in the paper and is associated wth increase in mean F0 (pitch), rate of articulation and volume. 
#### 4. Joy
Joy is associated with high volume and a slight increase in mean F0 (pitch). 
#### 5. Sadness
Sadness is associated with a decrease in all 3 considered prosodic elements. 

Although the paper actually contains calculated data modelling the exact changes, their direct applicability on synthetic voices found in GCP is very minimal, as the base mean F0 and variance of F0, data crucial to calculate the exact shifts numerically, aren't available. Thus, their values are used to infer the relative changes of prosody among different emotions (for example that the increase in F0 is higher in fear than in anger, etc) and the final choice of the exact values are a result of both the study and extensive trial and error. The research paper also models the speech contour parameters and MFCCs, which can't be modelled using SSML or in fact any popular TTS engines as that level of micro control is usually left to the underlying Neural Networks than explicit programming.  

  
*Note: 1. Surprise is encoded to cause a significant increase in rate and moderate increase in pitch and loudness. This is based on my own observation and trial-and-error as the research paper didn't explicitly contain the emotion in its study.  
       2. Neutrality is encoded to have default values for all.*  

Further, when the text contains multiple sentences, <break/> tags are inserted in between with the least duration for fear, highest for sadness and values in between for others to reflect the rate of articulation values for them found in the study. 

### main.py
This file contains the backend code for the FastAPI app and uses the other two Python scripts to call the pipeline. 

### config.json
This file contains the changes in vocal parameters for each emotion. 
