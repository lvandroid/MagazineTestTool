import subprocess
from constants import *
import cmd as CMD
import shlex

from flet import (
    UserControl,
    Column,
    Row,
    Text,
    OutlinedButton,
    ElevatedButton,
    TextButton,
    FilledButton,
    Container,
    TextField,
    MainAxisAlignment,
    Markdown,
    MarkdownExtensionSet,
    Divider,
    Slider,
    margin,
    GridView,
    colors
)


class TestSpace(UserControl):
    def build(self):
        self.log_view = TextField("", text_size=12, height=600, expand=True, multiline=True, read_only=True,
                                  autofocus=True)
        return Column([
            Row([
                Column([
                    TextButton(text="重新挂载", on_click=lambda e: self.remount()),
                    TextButton(text="重启并重新挂载", on_click=lambda e: self.reboot_remount()),
                    TextButton(text="ROOT手机", on_click=lambda e: self.vivoroot()),
                    TextButton(text="切换测试环境", on_click=lambda e: self.choose_overseas_test_host()),
                    TextButton(text="切换正式环境", on_click=lambda e: self.choose_overseas_normal_host()),
                    TextButton(text="清除阅图数据", on_click=lambda e: self.clean_magazine_data()),
                ]),
                Column([
                    TextButton(text="卸载最新版本", on_click=lambda e: self.uninstall_magazine()),
                    TextButton(text="重启阅图", on_click=lambda e: self.restart_magazine()),
                    TextButton(text="打开http的log", on_click=lambda e: self.update_http_log(True)),
                    TextButton(text="关闭http的log", on_click=lambda e: self.update_http_log(False)),
                    TextButton(text="放开手机log限制", on_click=lambda e: self.open_log()),
                    TextButton(text="清空控制台", on_click=lambda e: self.clean_log())
                ])

            ]),
            self.log_view
        ])

    def remount(self):
        self.execute_commands(CMD.ADB_REMOUNT)

    def reboot_remount(self):
        self.execute_commands(CMD.ADB_REBOOT_REMOUNT)

    def vivoroot(self):
        self.execute_commands(CMD.ADB_VIVO_ROOT)

    def choose_overseas_test_host(self):
        self.execute_commands(CMD.OVERSEAS_TEST_HOST)

    def choose_overseas_normal_host(self):
        self.execute_commands(CMD.OVERSEAS_NORMAL_HOST)

    def clean_magazine_data(self):
        self.execute_commands(CMD.ADB_CLEAR_MAGAZINE_DATA)

    def open_log(self):
        self.execute_commands(CMD.ADB_OPEN_LOG)

    def uninstall_magazine(self):
        self.execute_commands(CMD.ADB_UNINSTALL)

    def restart_magazine(self):
        self.execute_commands(CMD.RESTART_MAGAZINE)

    def update_http_log(self, open):
        cmd = CMD.OPEN_OKHTTP_LOG if open else CMD.CLOSE_OKHTTP_LOG
        self.execute_commands(cmd)

    def exec_cmd(self, cmd):
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
                                creationflags=subprocess.CREATE_NO_WINDOW)
        # 获取标准输出和标准错误
        stdout_output = result.stdout
        stderr_output = result.stderr

        # 检查命令是否成功执行
        if result.returncode == 0:
            # 打印标准输出
            self.log_view.value = f"{self.log_view.value}\n{stdout_output}"
        else:
            # 如果命令执行失败，可以打印错误信息
            self.log_view.value = f"{self.log_view.value}\n{stderr_output}"
        self.log_view.update()

    def execute_commands(self, cmds):
        for cmd in cmds:
            c = shlex.split(cmd)
            self.log_view.value = f"{self.log_view.value}\n{cmd}"
            self.log_view.update()
            self.exec_cmd(c)

    def clean_log(self):
        self.log_view.value = ""
        self.log_view.update()