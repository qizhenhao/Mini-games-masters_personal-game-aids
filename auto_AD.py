import mouse 
import keyboard
import time
import sys


#--------------------------变量定义--------------------------


view = 'enable'

tag = 'HuangYouGaoShou'

clickTime = 0.1 # 默认0.1秒的时间间隔
clickCount = 10 # 连点次数
clickBlock = False # 设置阻塞模式， 默认是关的，不阻塞点几下就增加几下，开启后连续点不能累计

#-------------------框架函数----------------------
def my_help():
    print(' ?: 查看所有指令')    
    print(' exit: 退到上一个视图')

def help_enable():
    print(' connector: 进入连点器视图并且开启连点器任务，提供配置连点器配置 【点击鼠标侧键执行一次连点任务】')

def help_connector():
    print(' time (0.0-10.0]: 连点任务中的操作的时间间隔')
    print(' count (1-1000): 单次操作的次数')
    print(' [no] block: 设置阻塞模式， 默认是关的，不阻塞点几下就增加几下，开启后连续点不能累计')
    print(' show config: 查看当前视图下的配置')

def show_config_connector():
    print('!connector')
    print(' time ' + str(clickTime))
    print(' count ' + str(clickCount))
    print(' block' if clickBlock else ' no block')
    print('!')

def enable():
    global view
    print(tag + '#', end='')
    command = input().lstrip().rstrip()
    if command == 'exit':
        print(' 拜拜！ ')
        sys.exit(0)
    elif command == '?':
        my_help()
        help_enable()
        return ''
    elif command == 'connector':
        view = 'connector'
        mouse.hook(connector_handler)
        print('点击鼠标侧键触发一次连点器')
        return ''
    return command

def connector():
    global view, clickTime, clickCount, clickBlock
    # 修改视图， 修改点击的时间间隔， 修改连点次数
    print(tag + '(connector)#', end='')
    command = input().lstrip().rstrip()
    if command == 'exit':
        view = 'enable'
        mouse.unhook(connector_handler)
        return ''
    elif command == '?':
        my_help()
        help_connector()
        return ''
    elif command.startswith('time '):
        try:
            t = float(command[5:])
            if not (t > 0 and t < 10):
                raise '时间不能为负数'
            clickTime = t
            print('设置成功！时间间隔为：', clickTime)
            return ''
        except Exception as e:
            pass
    elif command.startswith('count '):
        try:
            t = int(command[6:])
            if not (t >= 1 and t <= 1000):
                raise '不符合规定'
            clickCount = t
            print('设置成功！点击次数为：', clickCount)
            return ''
        except Exception as e:
            pass
    elif command == 'show config':
        show_config_connector()
        return ''
    elif command == 'no block':
        clickBlock = False
        return ''
    elif command == 'block':
        clickBlock = True
        return ''
    return command
#------------------------定义映射-------------------------------
views = {
    'enable': enable,
    'connector': connector,
}

#--------------------------功能实现----------------------------
def connector_handler(event):
    if isinstance(event, mouse.ButtonEvent):
        if event.button == 'x':
            for _ in range(clickCount):
                mouse.click()
                time.sleep(clickTime)
            if clickBlock:
                # 点一次生效一次
                q = mouse._listener.queue
                while not q.empty():
                    item = q.get()
            return True
    return False

#--------------------------程序入口-----------------------------
while True:
    command = views[view]()
    if command == 'abort':
        print(' 加纳！ ')
        sys.exit(0)
    elif command != '':
        print('当前输入的指令不正确或者不存在！')

