import os
import threading

from play import play
from sounds import sounds
from kb_listen import Listener

from pywebio.pin import *
from pywebio.output import *
from pywebio.session import *
from pywebio.input import actions
from pywebio import config, start_server

# 应用设置
config(title='🐔音盒', description='一个基于PYWEBIO的趣味音频播放软件', theme='minty')


s = sounds() # 音频文件获取与处理
p = play(s) # 音频文件的播放
kb_ls = Listener(s, p) # 键盘监听与处理

# 键盘扩展选项
kb_op = [dict(label='🧲开启键盘绑定模式', value='binding-mode',selected=False, disabled=False),
        dict(label='🎧开启键盘监听', value='listen-mode',selected=False, disabled=False),
        dict(label='🤪未绑定的按键随机播放', value='r-mode', selected=True, disabled=False)]
        #  dict(label='⏱切歌暂停(暂未实现)', value='block-mode', selected=False, disabled=True)
binding_mode_stm = False # 是否处于键盘绑定模式

def save_binding():
    with popup(title='保存'):
        put_markdown('> 请输入文件名')
        put_input(name='save-filename',value='savename')
        def sava_and_quit():
            kb_ls.sava(pin['save-filename'])
            close_popup()
            toast('保存成功！')
        put_button(label='确认',onclick=lambda :sava_and_quit())

def load_binding():
    with popup(title='读取'):
        put_markdown('## 在data文件夹下读取到以下文件：')
        put_markdown('> 请选择要读取的文件')
        def load_and_quit(filename:str):
            kb_ls.load(filename)
            toast('读取成功！')
            close_popup()
        put_buttons(buttons=kb_ls.save_files, onclick=lambda _:load_and_quit(_))


def kb_binding(value):
    with popup(title='添加按键绑定'):
        put_markdown(f'## 请输入语音`{value.split(".")[0]}`对应的按键名称'),
        put_input(name='key', label='')
        put_markdown('''
> 例如

- `a` ` 当按下 a 键时播放 `
- `A` ` 按下 shift + a 或者开启大写状态下按下 a 时播放 `
- `space` ` 按空格键播放 `''')
        put_text('当前已绑定的按键,点击以删除：')
        put_scope('binded-keys-show')
        # 当前 语音 的键盘绑定情况字典类型{ key:musci, ...}
        def get_cur_music_binded_keys() ->list: # 获取当前语音绑定按键列表
            nonlocal value
            res = []
            for k,v in kb_ls.key_map[p.current_pack].items():
                if v == value:
                    res.append(k)
            return res
        # 展示已绑定的按键
        def show_binded_keys_show():
            with use_scope('binded-keys-show',clear=True):
                put_buttons(get_cur_music_binded_keys(), delete_key, small=True)
        # 删除指定按钮
        def delete_key(key_):
            del kb_ls.key_map[p.current_pack][key_]
            toast(content=f'成功解绑按键：{key_}')
            show_binded_keys_show()
        def sava_and_quit(): 
            key = pin['key'] # 获取用户输入
            nonlocal value
            if key in get_cur_music_binded_keys():
                toast('按键重复设置！', color='warn')
                return
            if key in kb_ls.key_map[p.current_pack].keys():
                toast(f'该按键已绑定语音{kb_ls.key_map[p.current_pack][key].split(".")[0]}，请检查并重新设置', 4, color='warn')
                return
            if key == '':
                toast('请输入按键！', color='warn')
                return
            kb_ls.key_map[p.current_pack][key] = value
            close_popup()
        show_binded_keys_show()
        put_html('<hr>')
        put_button(label='确认', onclick=sava_and_quit)


# 更新语言包,并在指定scope列出语言包内容
def show_sounds(pack_name=None, scope_name='sound-buttons', color='primary',
                callback=lambda name: p.play_sound_by_name(name)):
    # 为空则维持不变
    if pack_name is not None:
        p.current_pack = pack_name
    # 如果处于绑定模式则按照绑定模式来输出
    if binding_mode_stm:
        callback = kb_binding
        color='danger'
    # 按钮属性
    button_attri = [dict(label=name.split('.')[0], value=name, color=color)
                    for name in s.get_sounds_ditc()[p.current_pack]]
    with use_scope(scope_name,clear=True):
        put_buttons(buttons=button_attri, onclick=callback)


# 用户界面
def user_ui():
    put_markdown('# 🐔音盒')
    put_collapse('语音包选择', put_buttons(
        s.get_packs_name(), onclick=show_sounds), open=True)
    put_scope('pack-seleted-info')  # 输出选择中的语言包
    put_collapse(title='高级', content=[put_row(
        [put_checkbox(name=opt['value'], options=[opt['label']]) for opt in kb_op]+
        [put_button(label='读取绑定记录', onclick=load_binding, small=True, outline=True),None] +
        [put_button(label='保存绑定记录', onclick=save_binding, small=True, outline=True)]
    ,size=r'24% 22% 26% 13% 2% 13%')], open=False)
    put_scope('sound-buttons') # 按钮展示区
    # 监听高级选项
    advance_kb_opts()


checkbox_listen = True
# 监听高级选项，响应变动
def advance_kb_opts():
    kb_binding_checkbox_thr = threading.Thread(target=kb_binding_checkbox)
    kb_listen_checkbox_thr = threading.Thread(target=kb_listen_checkbox)
    random_play_checkbox_thr = threading.Thread(target=random_play_checkbox)
    register_thread(kb_binding_checkbox_thr)
    register_thread(kb_listen_checkbox_thr)
    register_thread(random_play_checkbox_thr)
    kb_binding_checkbox_thr.start()
    kb_listen_checkbox_thr.start()
    random_play_checkbox_thr.start()
    run_js('document.querySelector("body > footer").innerHTML = content',
        content='\n\t🐔音盒，一个基于<a href="https://www.pyweb.io/" target="_blank">PyWebIO</a>的趣味音频播放软件\t\n')

# 对‘开启键盘绑定模式’checkbox进行监听
def kb_binding_checkbox():
    global binding_mode_stm
    while True:
        if not checkbox_listen:
            break
        # 如果用户勾选
        if len(pin_wait_change('binding-mode')['value']) != 0:
            toast(content='点击下方按钮可进行绑定和查看已绑定的按键',duration=3.5, position='right', color='warn')
            binding_mode_stm = True
        else:
            binding_mode_stm = False
        show_sounds()

# 对“开启键盘监听”checkbox进行监听
def kb_listen_checkbox():
    while True:
        if not checkbox_listen:
            break
        if len(pin_wait_change('listen-mode')['value']) != 0:
            kb_ls.listen_config['listen-mode'] = True
            # toast(content='listen-mode')
        else:
            kb_ls.listen_config['listen-mode'] = False

# 对“未绑定时随机播放”checkbox进行监听
def random_play_checkbox():
    while True:
        if not checkbox_listen:
            break
        if len(pin_wait_change('r-mode')['value']) != 0:
            kb_ls.listen_config['r-mode'] = True
            # toast('r-mode')
        else:
            kb_ls.listen_config['r-mode'] = False

def main():
    user_ui()
    @defer_call
    def clear():
        kb_ls.listen_config['listen-mode'] = False
        checkbox_listen = False
        os._exit(0)

if __name__ == '__main__':
    # 调试
    # start_server(main, port=80, host='0.0.0.0',
    #             debug=1, auto_open_webbrowser=False)
    main()