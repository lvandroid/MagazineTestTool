import logging, os, sys, json

from flet import (
    Page, SnackBar, Text,
)

import subprocess

def show_toast(page: Page, msg):
    snack_bar = SnackBar(content=Text(msg), duration=1000)
    page.snack_bar = snack_bar
    page.snack_bar.open = True
    page.update()

def exec_cmd(cmds):
    for cmd in cmds:
        logging.debug(cmd)
        c = cmd.split()
        result = subprocess.run(c, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, text=True,
                       creationflags=subprocess.CREATE_NO_WINDOW)
        # 获取标准输出和标准错误
        stdout_output = result.stdout
        stderr_output = result.stderr

        # 检查命令是否成功执行
        if result.returncode == -1:
            # 打印标准输出
            logging.error(stderr_output)
        else:
            logging.debug(stdout_output)

def get_conf_path():
    if getattr(sys, 'frozen', False):
        # 如果程序被打包，则使用可执行文件所在的目录
        application_path = os.path.dirname(sys.executable)
    else:
        # 如果程序未被打包，则使用__file__所在的目录
        application_path = os.path.dirname(os.path.realpath(__file__))
    return application_path

def get_config_path():
    # 构建配置文件的路径
    config_path = os.path.join(get_conf_path(), "conf", "config.json")
    return config_path

def load_json_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)