from google import genai
from config import GEMINI_API_KEY

client = genai.Client(api_key=GEMINI_API_KEY)

def voice_to_text(audio_file_path):
    try:
        with open(audio_file_path, "rb") as audio:
            audio_bytes = audio.read()
        result = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[
            {
                "inline_data": {
                    "mime_type": "audio/ogg",
                    "data": audio_bytes
                }
            },
            "Convert this audio into text only.",
        ]
    )
        if not result or not result.text.strip():
            return "❌ Sorry, I couldn't understand the audio clearly."

        return result.text

    except Exception as e:
        return "⚠️ Something went wrong while processing the audio."

