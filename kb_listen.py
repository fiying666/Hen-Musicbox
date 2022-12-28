import os
import json
import random
import keyboard
import threading

from play import play
from sounds import sounds


class Listener:
    """
    ## 记录键盘绑定
    ```py
    {
        "pack":(str) 语音包名称:
        {
        "key":(str) 按键名称 : "value":(str) 语音名称(全名,比如aaa.mp3),
        etc...
        },
        etc...
    }```
    """
    def __init__(self, sd:sounds = None, pl:play = None):
        self.key_map = dict(zip(
            sd.get_packs_name(),
            [{} for _ in range(len(sd.get_packs_name()))]
        ))
        # 监听设置
        self.listen_config = {'listen-mode':False, 'r-mode':False}
        # 读取已保存的文件
        self.save_files = os.listdir('.\\data\\')
        self.play = pl
        self.sound = sd
        threading.Thread(target=self.k_v_matching).start()

    def k_v_matching(self):
        def callback(e):
            nonlocal self
            if self.listen_config['listen-mode']:
                # 以当前语言包来获取
                binding_ditc = self.key_map[self.play.current_pack]
                if e.event_type == 'down':
                    if e.name in binding_ditc.keys():
                        self.play.play_sound_by_name(binding_ditc[e.name])
                    elif self.listen_config['r-mode']: 
                        self.play.play_sound_by_name(
                            random.choice(
                                self.sound.get_sounds_ditc()[self.play.current_pack]))
        keyboard.hook(callback)
        keyboard.wait()


    def refresh_save_files(self):
        self.save_files = os.listdir('.\\data\\')

    def load(self, filename:str):
        with open(file=f'.\\data\\{filename}',mode='r',encoding='utf-8') as f:
            self.key_map = json.loads(f.read())

    def sava(self, filename:str = 'save'):
        data = json.dumps(self.key_map)
        with open(file=f'.\\data\\{filename + ".json"}', mode='w', encoding='utf-8') as f:
            f.write(data)
        self.refresh_save_files()