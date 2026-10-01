import os
import base64
import asyncio

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, Response
from pydantic import BaseModel
from google import genai

from src.agent.screening_agent import ScreeningAgent

load_dotenv()


app = FastAPI()

agent = ScreeningAgent()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

TTS_MODEL = os.getenv(
    "GEMINI_TTS_MODEL",
    "gemini-3.8-flash-lite-tts"
)

lock = asyncio.Lock()


class ChatRequest(BaseModel):
    message: str


class TTSRequest(BaseModel):
    text: str


@app.get("/", response_class=HTMLResponse)
async def home():

    return """
<!DOCTYPE html>
<html>

<head>

<title>Candidate Screening AI</title>

<style>

body {
    font-family: Arial;
    max-width: 700px;
    margin: 40px auto;
    padding: 20px;
}

#chat {
    border: 1px solid #ddd;
    padding: 15px;
    min-height: 300px;
    margin-bottom: 15px;
}

.message {
    margin: 12px 0;
}

textarea {
    width: 100%;
    height: 70px;
    padding: 10px;
    box-sizing: border-box;
}

button {
    padding: 10px 16px;
    margin-top: 10px;
    margin-right: 5px;
}

</style>

</head>

<body>

<h1>Candidate Screening AI</h1>

<div id="status">Ready</div>

<div id="chat"></div>

<textarea
    id="message"
    placeholder="Speak or type your message..."
></textarea>

<br>

<button id="mic">🎤 Speak</button>

<button id="send">Send</button>


<script>

const messageBox =
    document.getElementById("message");

const chat =
    document.getElementById("chat");

const status =
    document.getElementById("status");

const micButton =
    document.getElementById("mic");

const sendButton =
    document.getElementById("send");


/* ---------- STT ---------- */

const SpeechRecognition =
    window.SpeechRecognition ||
    window.webkitSpeechRecognition;

let recognition = null;

let listening = false;

let manuallyStopped = false;

let finalText = "";


if (SpeechRecognition) {

    recognition = new SpeechRecognition();

    recognition.lang = "en-IN";

    recognition.continuous = true;

    recognition.interimResults = true;


    recognition.onstart = () => {

        listening = true;

        micButton.textContent =
            "⏹ Stop";

        status.textContent =
            "Listening...";
    };


    recognition.onresult = (event) => {

        let interim = "";

        for (
            let i = event.resultIndex;
            i < event.results.length;
            i++
        ) {

            const text =
                event.results[i][0].transcript;

            if (event.results[i].isFinal) {

                finalText += text + " ";

            } else {

                interim += text;
            }
        }

        messageBox.value =
            (finalText + interim).trim();
    };


    recognition.onerror = (event) => {

        console.log(
            "STT error:",
            event.error
        );

        if (event.error === "not-allowed") {

            manuallyStopped = true;

            status.textContent =
                "Microphone permission denied.";
        }
    };


    recognition.onend = () => {

        if (
            !manuallyStopped &&
            listening
        ) {

            setTimeout(() => {

                try {

                    recognition.start();

                } catch (e) {

                    console.log(e);
                }

            }, 300);

            return;
        }

        listening = false;

        micButton.textContent =
            "🎤 Speak";

        status.textContent =
            "Ready";
    };
}


micButton.onclick = () => {

    if (!recognition) {

        status.textContent =
            "Speech recognition is not supported.";

        return;
    }


    if (listening) {

        manuallyStopped = true;

        listening = false;

        recognition.stop();

        micButton.textContent =
            "🎤 Speak";

        status.textContent =
            "Recording stopped.";

        return;
    }


    finalText = "";

    messageBox.value = "";

    manuallyStopped = false;

    try {

        recognition.start();

    } catch (e) {

        console.log(e);
    }
};


/* ---------- CHAT ---------- */

function addMessage(sender, text) {

    const div =
        document.createElement("div");

    div.className = "message";

    div.innerHTML =
        "<b>" +
        sender +
        ":</b> " +
        text;

    chat.appendChild(div);

    chat.scrollTop =
        chat.scrollHeight;
}


/* ---------- GEMINI TTS ---------- */

async function speak(text) {

    status.textContent =
        "Generating voice...";

    const response =
        await fetch("/tts", {

            method: "POST",

            headers: {
                "Content-Type":
                    "application/json"
            },

            body: JSON.stringify({
                text: text
            })
        });


    if (!response.ok) {

        throw new Error(
            await response.text()
        );
    }


    const blob =
        await response.blob();

    const url =
        URL.createObjectURL(blob);

    const audio =
        new Audio(url);


    audio.onplay = () => {

        status.textContent =
            "Agent is speaking...";
    };


    audio.onended = () => {

        URL.revokeObjectURL(url);

        status.textContent =
            "Ready";
    };


    audio.onerror = () => {

        URL.revokeObjectURL(url);

        status.textContent =
            "Audio playback error.";
    };


    await audio.play();
}


/* ---------- SEND ---------- */

async function sendMessage() {

    const text =
        messageBox.value.trim();

    if (!text) {
        return;
    }


    if (listening) {

        manuallyStopped = true;

        listening = false;

        try {

            recognition.stop();

        } catch (e) {

            console.log(e);
        }
    }


    addMessage(
        "You",
        text
    );

    messageBox.value = "";

    status.textContent =
        "Agent is thinking...";


    try {

        const response =
            await fetch(
                "/chat",
                {

                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        message: text
                    })
                }
            );


        const data =
            await response.json();


        if (!response.ok) {

            throw new Error(
                data.detail ||
                "Server error"
            );
        }


        addMessage(
            "Agent",
            data.response
        );


        await speak(
            data.response
        );


    } catch (error) {

        console.error(error);

        status.textContent =
            "Error";

        addMessage(
            "Agent",
            "Sorry, something went wrong."
        );
    }
}


sendButton.onclick =
    sendMessage;


messageBox.addEventListener(
    "keydown",
    (event) => {

        if (
            event.key === "Enter" &&
            !event.shiftKey
        ) {

            event.preventDefault();

            sendMessage();
        }
    }
);

</script>

</body>

</html>
"""


@app.post("/chat")
async def chat(request: ChatRequest):

    async with lock:

        try:

            return agent.respond(
                request.message
            )

        except Exception as e:

            print(
                "CHAT ERROR:",
                repr(e)
            )

            raise HTTPException(
                status_code=500,
                detail=str(e)
            )


@app.post("/tts")
async def tts(request: TTSRequest):

    try:

        response = client.models.generate_content(
            model=TTS_MODEL,

            contents=request.text,

            config={
                "response_modalities": ["AUDIO"],

                "speech_config": {
                    "voice_config": {
                        "prebuilt_voice_config": {
                            "voice_name": "Kore"
                        }
                    }
                }
            }
        )


        audio_data = None


        for candidate in response.candidates:

            if not candidate.content:
                continue

            for part in candidate.content.parts:

                if part.inline_data:

                    audio_data = (
                        part.inline_data.data
                    )

                    break

            if audio_data:
                break


        if not audio_data:

            raise RuntimeError(
                "No audio returned by Gemini."
            )


        if isinstance(
            audio_data,
            str
        ):

            audio_data = base64.b64decode(
                audio_data
            )


        return Response(
            content=audio_data,
            media_type="audio/wav"
        )


    except Exception as e:

        print(
            "TTS ERROR:",
            repr(e)
        )

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )