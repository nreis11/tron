import os


class Sound:
    def start_music(self, name, is_game_on=False):
        self.stop_music()
        if os.name == "posix":
            os.system(f"afplay sounds/{name}.wav&")
            if is_game_on:
                os.system("say grid is live!&")
        elif os.name == "nt":
            winsound.PlaySound(bgm, winsound.SND_ASYNC)

    def stop_music(self):
        if os.name == "posix":
            os.system("killall afplay")
        elif os.name == "nt":
            winsound.PlaySound(None, winsound.SND_PURGE)

    def play_sfx(self, sound):
        if os.name == "posix":
            os.system(f"afplay sounds/{sound}.wav&")
        elif os.name == "nt":
            # winsound.PlaySound(sound, winsound.SND_ASYNC)
            # can't play simoutaneous sounds
            pass
