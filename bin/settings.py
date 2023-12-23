import json
import logging
import os
from cmd import (
    execute_commands
)

from flet import (
    UserControl,
    Column,
    Row,
    TextField,
    ElevatedButton,
)


class Settings(UserControl):

    def build(self):
        self.log_view = TextField(width=300)
        self.cmd_panel = Column(
            [
                # ElevatedButton(text="新增adb命令", on_click=lambda e: self.add_adb()),
                # ElevatedButton(text="加载设置配置", on_click=lambda e: self.loading_settings()),
            ], expand=True
        )
        result = Row([
            self.log_view,
            self.cmd_panel
        ], expand=True)
        return result

    def add_adb(self):
        pass
