import mutagen.mp3


class Song:
    # This code is from HQMediaPlayer, my media player.
    ARTIST = "artist"
    TITLE = "title"
    ALBUM = "album"

    def __init__(self, file_location: str):
        self.file_location = file_location
        self.mp3 = mutagen.mp3.EasyMP3(file_location)

    def __str__(self):
        return self.file_location

    def has_song(self):
        return self.file_location is not None

    def get_info(self, wanted_info: str = TITLE):
        """Gets the desired metadata from the mp3 file.

        :return: Metadata in string form.
        """
        try:
            info = str(self.mp3[wanted_info])
            return info[2:len(info) - 2]  # Removes the ['']
        except KeyError:
            return "N/A"

    def get_duration(self):
        """

        :return: The song's true duration in milliseconds.
        """
        return int(self.mp3.info.length * 1000)
