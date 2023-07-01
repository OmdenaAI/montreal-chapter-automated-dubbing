from moviepy.editor import VideoFileClip, AudioFileClip
import os
from pydub import AudioSegment
import tempfile
from typing import Dict


class DubbingProcessor:
    def join_audio_segments(self, translated_audio_dict: Dict) -> AudioSegment:
        """
        Simply joins all segments into a new AudioSegment, taking in consideration the original start time of each
        segment.

        Parameters:
        -----------
        translated_audio_dict: dict

        Returns:
        --------
        AudioSegment
        """
        # creates an empty audio segment,
        original_length = translated_audio_dict['segments'][-1]['end']
        new_full_audio = AudioSegment.silent(duration=original_length * 1000)

        for segment in translated_audio_dict['segments']:
            new_full_audio = new_full_audio.overlay(segment['audio'], position=segment['start'] * 1000)

        return new_full_audio

    def add_audio_to_video(self, video_path: str, new_audio: AudioSegment) -> str:
        """
        Replaces the translated audio in the video, creating a new MP4 file.

        Parameters:
        -----------
        video_path: str

        new_audio: AudioSegment

        Returns:
        --------
        str
        """

        # Load the MP4 video file
        video_clip = VideoFileClip(video_path)

        # Get the duration of the video
        video_duration = video_clip.duration * 1000

        # Adjust the length of the new audio to match the video duration
        if len(new_audio) > video_duration:
            # If the new audio is longer, truncate it
            new_audio = new_audio[:video_duration]
        elif len(new_audio) < video_duration:
            # If the new audio is shorter, add a silent segment at the end
            silence = AudioSegment.silent(duration=len(new_audio) - video_duration)
            new_audio = new_audio[:video_duration] + silence

        with tempfile.TemporaryDirectory() as tmp_dir_name:
            temp_file_path = os.path.join(tmp_dir_name, "temp_audio.mp3")
            new_audio.export(temp_file_path, format="mp3")
            audio_clip = AudioFileClip(temp_file_path)

            # Concatenate the video clip with the audio clip
            final_clip = video_clip.set_audio(audio_clip)

        # Append "_dubbed" to the video filename
        directory, filename = os.path.split(video_path)
        base_name, extension = os.path.splitext(filename)
        new_base_name = base_name + "_dubbed"
        new_video_path = os.path.join(directory, new_base_name + extension)

        # Write the video clip with the replaced audio to the output file
        final_clip.write_videofile(new_video_path)

        # Close the video clips
        video_clip.close()
        final_clip.close()

        return new_video_path
