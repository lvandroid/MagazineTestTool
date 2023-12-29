import json
import os
import time

from flet import (
    UserControl,
    Column,
    Row,
    TextField,
    ElevatedButton,
    MainAxisAlignment,
    CrossAxisAlignment,
    Text,
    TextButton,
    AlertDialog,

)


class Settings(UserControl):

    def build(self):
        result = Row([
            ElevatedButton("新增Tab", on_click=lambda e: self.add_tab_dialog())
        ], expand=True, vertical_alignment=CrossAxisAlignment.START)
        return result

    def update_dialog(self, is_open):
        self.dialog.open = is_open
        self.dialog.update()

    def add_tab_dialog(self):
        tab_name_input = TextField(label="Tab Name", hint_text="请输入tab的名称", autofocus=True, width=200)
        self.dialog = AlertDialog(
            content=Column([tab_name_input]),
            actions=[
                ElevatedButton("确认", on_click=lambda e: self.create_tab(tab_name_input.value)),
                TextButton("取消", on_click=lambda e: self.update_dialog(False))
            ]
        )
        self.update_dialog(True)

    def create_tab(self, tab_name):
        if len(tab_name) == 0:
            return
            # 生成当前时间戳命名的文件
        timestamp = int(time.time())
        new_file_name = f"{timestamp}.json"
        new_file_path = os.path.join("conf", new_file_name)
        # 定义新的JSON文件的初始内容
        new_content = {
            "tab_name": tab_name,
            "scripts": [
                {
                    "title": "log",
                    "cmds": ["git log"]
                },
                {
                    "title": "pull",
                    "cmds": ["git pull --rebase"]
                }
            ]
        }

        # 创建新的JSON文件
        with open(new_file_path, "w") as new_file:
            json.dump(new_content, new_file, indent=4)

        # 更新config.json
        config_path = os.path.join("conf", "config.json")
        with open(config_path, "r") as config_file:
            config = json.load(config_file)

        config["tabs"].append({"tab_name": tab_name, "conf_path": new_file_path})
        with open(config_path) as config_file:
            json.dump(config, config_file, indent=4)
        self.update_dialog(False)
