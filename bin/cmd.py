from constants import *
import subprocess
import time
import datetime
import os

# ADB_UNINSTALL = [ADB, "uninstall", MAGAZINE_PKG_NAME] #卸载当前阅图版本
ADB_UNINSTALL = ["adb uninstall com.vivo.magazine"]
ADB_CLEAR_MAGAZINE_DATA = [  # 清除阅图缓存数据：包括SP，数据库等信息
    "adb shell pm clear com.vivo.magazine",
    "adb shell setprop debug.festival.config yes",
    "adb shell am force_stop com.vivo.magazine"
]
# ADB_CLEAR_MAGAZINE_DATA= [ #清除阅图缓存数据：包括SP，数据库等信息
# [ADB, PM, "clear", MAGAZINE_PKG_NAME],
# [ADB,SHELL,SET_PROP,"debug.festival.config", YES],
# [ADB, SHELL,AM, "stopforce-stop", MAGAZINE_PKG_NAME]
# ]
ADB_REMOUNT = [ADB, REMOUNT]
ADB_REMOUNT = ["adb remount"]
# ADB_REBOOT_REMOUNT=[ADB, REBOOT, REMOUNT]
ADB_REBOOT_REMOUNT = ["adb reboot remount"]
ADB_OPEN_LOG = [  # 放开log限制
    "adb shell setprop persist.sys.log.ctrl yes",
    "adb shell setprop persist.sys.ratelimit 0",
    "adb shell setprop log.ratelimit.level 0"
]
# ADB_OPEN_LOG= [ #放开log限制
# [ADB, SHELL, SET_PROP, "persist.sys.log.ctrl", YES],
# [ADB, SHELL, SET_PROP, "persist.sys.ratelimit", 0],
# [ADB, SHELL, SET_PROP, "log.ratelimit.level", 0]
# ]
# ADB_VIVO_ROOT= [ADB, VIVO_ROOT]
ADB_VIVO_ROOT = ["adb vivoroot"]
ADB_SHELL = ["adb shell"]
# ADB_SHELL = [ADB, SHELL]
OVERSEAS_TEST_HOST = [  # 切换到外销测试环境
    "adb shell setprop dev.magazine.testhost yes",
    "adb shell setprop dev.magazine.ad_test_host 10.101.102.107:8080",
    "adb shell setprop dev.magazine.testhost_push_guide yes",
    # "adb shell setprop dev.magazine.test_url http://skyrealm-test.vivo.com.cn:8080",
    "adb shell setprop dev.magazine.test_url http://10.101.28.199:8080",
    "adb shell setprop persist.sys.log.ctrl yes"
]
# OVERSEAS_TEST_HOST = [ #切换到外销测试环境
# [ADB, SHELL, SET_PROP, "dev.magazine.testhost", YES],
# [ADB, SHELL, SET_PROP, "dev.magazine.ad_test_host", YES],
# [ADB, SHELL, SET_PROP, "dev.magazine.testhost_push_guide", YES]
# ]
OVERSEAS_NORMAL_HOST = [  # 切换到外销正式环境
    "adb shell setprop dev.magazine.testhost no",
    "adb shell setprop dev.magazine.ad_test_host no",
    "adb shell setprop dev.magazine.testhost_push_guide no",
    "adb shell setprop persist.sys.log.ctrl no"
]
# OVERSEAS_NORMAL_HOST= [ #切换到外销正式环境
#     [ADB, SHELL, SET_PROP, "dev.magazine.testhost", NO],
#     [ADB, SHELL, SET_PROP, "dev.magazine.ad_test_host", NO],
#     [ADB, SHELL, SET_PROP, "dev.magazine.testhost_push_guide", NO]
# ]
PRINT_MAGAZINE_LOG = [
    "adb shell",
    "logcat |grep _V_MS-"
]

OPEN_OKHTTP_LOG = [
    "adb shell setprop dev.magazine.okhttp.log yes"
]

CLOSE_OKHTTP_LOG = [
    "adb shell setprop dev.magazine.okhttp.log no"
]

RESTART_MAGAZINE = [
    "adb shell am force-stop com.vivo.magazine"
]


# 截屏并且将截图pull到当前目录，命名为当前时间包括时分秒的文件名
def screen_shot():
    image_folder = "image"
    if not os.path.exists(image_folder):
        os.makedirs(image_folder)

    # 获取当前时间作为文件名
    current_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

    # 截图命令
    screenshot_command = f'adb shell screencap -p /sdcard/{current_time}_screenshot.png'
    subprocess.run(screenshot_command, shell=True, creationflags=subprocess.CREATE_NO_WINDOW)

    # 将截图从设备复制到计算机
    pull_command = f'adb pull /sdcard/{current_time}_screenshot.png {image_folder}/'
    subprocess.run(pull_command, shell=True, creationflags=subprocess.CREATE_NO_WINDOW)


def screen_record():
    # 获取当前时间作为文件名
    current_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    # 录制视频命令
    record_command = f'adb shell screenrecord /sdcard/{current_time}.mp4'
    subprocess.Popen(record_command, shell=True)
    return current_time


def stop_screen_record(filename):
    # 停止录制视频命令
    stop_record_command = 'adb shell pkill -2 -f screenrecord'
    subprocess.run(stop_record_command, shell=True, creationflags=subprocess.CREATE_NO_WINDOW)

    video_folder = "video"
    if not os.path.exists(video_folder):
        os.makedirs(video_folder)

    # 将录制的视频从设备复制到计算机
    pull_video_command = f'adb pull /sdcard/{filename}.mp4 {video_folder}/'
    subprocess.run(pull_video_command, shell=True, creationflags=subprocess.CREATE_NO_WINDOW)


def clear_screenshots_and_videos():
    # 清除截图
    subprocess.run(['adb', 'shell', 'rm', '/sdcard/*.png'])

    # 清除录制的视频
    subprocess.run(['adb', 'shell', 'rm', '/sdcard/*.mp4'])
    # 删除本地截图文件（从image文件夹）
    image_folder = "image"
    for filename in os.listdir(image_folder):
        file_path = os.path.join(image_folder, filename)
        if filename.endswith(".png"):
            os.remove(file_path)

    # 删除本地录制的视频文件（从video文件夹）
    video_folder = "video"
    for filename in os.listdir(video_folder):
        file_path = os.path.join(video_folder, filename)
        if filename.endswith(".mp4"):
            os.remove(file_path)


def exec_cmd(cmd, log_view):
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, text=True,
                            creationflags=subprocess.CREATE_NO_WINDOW)
    # 获取标准输出和标准错误
    stdout_output = result.stdout
    stderr_output = result.stderr

    # 检查命令是否成功执行
    if result.returncode == -1:
        # 打印标准输出
        log_view.value = f"{log_view.value}\n{stdout_output}"
    else:
        # 如果命令执行失败，可以打印错误信息
        log_view.value = f"{log_view.value}\n{stderr_output}"
    log_view.update()


def execute_commands(cmds, log_view):
    for cmd in cmds:
        c = cmd.split()
        log_view.value = f"{log_view.value}\n{cmd}"
        log_view.update()
        exec_cmd(c, log_view)
        time.sleep(3)


def print_magazine_log(log_view):
    # 1. 执行adb shell
    adb_shell_command = "adb shell"
    shell_process = subprocess.run(adb_shell_command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
    # 2. 在adb shell中执行logcat | grep _V_MS-
    logcat_grep_command = "logcat | grep _V_MS-"
    shell_process.stdin.write(logcat_grep_command + "\n")
    shell_process.stdin.flush()
    # 读取adb shell中的输出
    output, error = shell_process.communicate()
    log_view.value += output
    log_view.update()