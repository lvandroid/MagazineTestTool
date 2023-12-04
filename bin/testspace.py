import subprocess
import constants as CONST
from cmd import ADB_CMD

from flet import (
    UserControl,
    Column,
    Row,
    Text,
    OutlinedButton,
    Container,
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
        self.log_view = Markdown(expand=True)
        return Column([GridView(
            [
                OutlinedButton(text="重新挂载", on_click=lambda e: self.remount()),
                OutlinedButton(text="ROOT手机", on_click=lambda e:self.vivoroot()),
                OutlinedButton(text="切换测试环境"),
                OutlinedButton(text="切换正式环境"),
                OutlinedButton(text="清除阅图数据"),
                OutlinedButton(text="清空log", on_click=lambda e: self.clean_log())
            ],
            runs_count=2,
            child_aspect_ratio=4,
            run_spacing=30,
            height=200, ),
            self.log_view
        ])

    def remount(self):
        self.exec_cmd(ADB_CMD[CONST.ADB_REMOUNT])

    def vivoroot(self):
        self.exec_cmd(ADB_CMD[CONST.ADB_VIVO_ROOT])

    def exec_cmd(self, cmd):
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        # 获取标准输出和标准错误
        stdout_output = result.stdout
        stderr_output = result.stderr

        # 检查命令是否成功执行
        if result.returncode == 0:
            # 打印标准输出
            self.log_view.value = f"{self.log_view.value}\n{stdout_output}```"
        else:
            # 如果命令执行失败，可以打印错误信息
            self.log_view.value = f"{self.log_view.value}\n{stderr_output}```"
        self.log_view.update()

    def clean_log(self):
        self.log_view.value = ""
        self.log_view.update()
