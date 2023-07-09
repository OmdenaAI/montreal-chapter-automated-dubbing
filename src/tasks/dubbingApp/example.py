import asyncio
import sys
from dubbing_app.dubbing_app import DubbingApp


async def main():
    # Get command-line arguments
    video_url = sys.argv[1]
    target_language = sys.argv[2]
    target_gender = sys.argv[3]

    app = DubbingApp()
    dubbed_video_url = await app.process_pipeline(video_url, target_language, target_gender)

    print(f"Dubbed video created here: {dubbed_video_url}")

    return dubbed_video_url

if __name__ == "__main__":
    # Run the main (coroutine)
    asyncio.run(main())
