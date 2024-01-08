import logging

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