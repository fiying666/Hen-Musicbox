import keyboard
import threading
from sounds import sounds
from playsound import playsound

# TEST

# 音频播放实现
class play:
    def __init__(self, sd: sounds = None):
        self.sounds = sd
        # 当前语言包
        self.current_pack = sd.get_packs_name()[0]
        self.blocking_mode = True  # 是否等待音频播放完成(未实现)
        pass

    def play_sound_by_name(self, music_name):
        threading.Thread(target=lambda: 
        playsound(self.sounds.packs_path + self.current_pack + '\\' + music_name)).start()
        pass
