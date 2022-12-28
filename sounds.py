import os
import string

# 获取并处理音频文件
class sounds:
    def __init__(self, path: string = '.\\src\\sounds\\'):
        self.packs_path = path  # 语音包路径
        self.packs = os.listdir(path)  
        # 每条语音的完整名字
        self.sounds_ditc = dict(zip(
            self.packs,
            [[sounds for sounds in os.listdir(path + pack)]
                for pack in self.packs]
        ))
    # 语音包列表
    def get_packs_name(self) -> list:
        return self.packs
    # 语言包以及对应的语音
    def get_sounds_ditc(self) -> dict:
        return self.sounds_ditc

