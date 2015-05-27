import os
import pygame

# NOTE: pygame.mixer seems to be eating CPU in the background,
# which is why it's repeatedly initialised and killed in here.

class Audio:
    SOUNDS_DIR = "sounds"
    DEFAULT_ALARM = "Default.wav"

    def __init__(self, settings):
        self._settings = settings

    def get_audio_files(self):
        try:
            return sorted([(os.path.splitext(f)[0], f)
                           for f in os.listdir(Audio.SOUNDS_DIR)
                           if os.path.isfile(os.path.join(Audio.SOUNDS_DIR, f))])
        except:
            return []

    def audio_test(self):
        self._play_alarm(False)

    def start_alarm(self):
        self._play_alarm(True)

    def stop(self):
        try:
            if pygame.mixer.get_init():
                pygame.mixer.music.stop()
                pygame.mixer.quit()
        except:
            pass

    def _play_alarm(self, loop):
        alarm_sound = self._settings["alarm_sound"]

        if not alarm_sound or not self._play_audio(alarm_sound, loop):
            self._play_audio(Audio.DEFAULT_ALARM, loop)

    def _play_audio(self, filename, loop = False):
        try:
            pygame.mixer.init()
            pygame.mixer.music.load(os.path.join(Audio.SOUNDS_DIR, filename))
            
            if loop:
                pygame.mixer.music.play(-1)
            else:
                pygame.mixer.music.play()
                
            return True

        except:
            print "WARNING: Couldn't play audio file '" + filename + "'."
            return False
