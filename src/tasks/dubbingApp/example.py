import sys
from dubbing_app.dubbing_app import DubbingApp

if __name__ == "__main__":
    # Get command-line arguments
    video_url = sys.argv[1]
    target_language = sys.argv[2]

    app = DubbingApp()
    dubbed_video_url = app.process_pipeline(video_url, target_language)

    print(f"Dubbed video created here: {dubbed_video_url}")
