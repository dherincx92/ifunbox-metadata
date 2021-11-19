import argparse
import os
import re
import sys
import subprocess

# when retrieving matches, we are guaranteed to have only one capture group
# due to using `(?:)``
MP3_TITLE_PATTERN = r"(?:content description\)\:)(.*?)\n"
MP4_TITLE_PATTERN = r"(?:Name\:)(.*?)\n"
EXCLUDE = ['.DS_Store']

class AudioFile:
    def __init__(self, file):
        self.file = file
        self.audio_type = os.path.splitext(self.file)[1]

    def get_audio_metadata(self):
        """
        Retrieves track title from running appropriate terminal commands

        Returns
        -------
        track_title: str
            Title of track
        """
        params = [self.file]

        command = ''
        if self.audio_type == '.m4a':
            command = 'mp4info'
            PATTERN = MP4_TITLE_PATTERN
        elif self.audio_type == '.mp3':
            command = 'id3info'
            PATTERN = MP3_TITLE_PATTERN
        params.insert(0, command)
        metadata = subprocess.run(
            params,
            encoding='utf-8', # ensures stdout is text and not bytes
            capture_output=True
        )
        title_match = re.search(PATTERN, metadata.stdout, re.DOTALL).groups()
        track_title = title_match[0].strip()
        return track_title


if __name__ == "__main__":
    audio_files_dir = '/Users/dherincx/Desktop/ifunbox_transfers'
    tree = os.walk(audio_files_dir)
    for dirpath, dirname, filenames in tree:
        for file in filenames:
            if file not in EXCLUDE:
                audio_file = AudioFile(os.path.join(dirpath, file))

