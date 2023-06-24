import asyncio
from text2speech_processor import Text2SpeechProcessor


async def main():
    processor = Text2SpeechProcessor()
    text_segments = [
        {"text": "How often do you think about space?", "start": 660, "end": 2700, "language": "en", "speaker_gender": "Female"},
        {"text": "Probably not enough considering how much we use it every day.", "start": 3320, "end": 6520, "language": "en", "speaker_gender": "Male"}
    ]
    target_language = "en"
    result = await processor.text_to_speech(text_segments, target_language)
    print(result)

if __name__ == "__main__":
    asyncio.run(main())

