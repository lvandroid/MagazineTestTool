import json
import logging
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

# 获取当前脚本所在的目录
curr_dir = os.path.dirname(os.path.realpath(__file__))


class Settings(UserControl):
    def __init__(self, page, on_create_tab):
        super().__init__()
        self.page = page
        self.on_create_tab = on_create_tab
        self.page = page
        self.tab_name_input = TextField(label="Tab Name", hint_text="请输入tab的名称", autofocus=True, width=200)
        self.command_rows = Column()  # 用于存放命令输入框的列
        self.dialog_content = Column([self.tab_name_input, self.command_rows])
        self.add_command_row()  # 初始时添加一组命令输入框

        self.dialog = AlertDialog(
            content=self.dialog_content,
            actions=[
                ElevatedButton("确认", on_click=lambda e: self.create_tab()),
                TextButton("取消", on_click=lambda e: self.update_dialog(False))
            ]
        )
        self.page.dialog = self.dialog

    def add_command_row(self):
        # 创建新的命令输入框
        title_input = TextField(label="Command Title", hint_text="请输入命令标题", width=200)
        cmd_input = TextField(label="Commands", hint_text="输入命令，多个命令用逗号隔开", width=200)
        self.command_rows.controls.append(Row([title_input, cmd_input, ElevatedButton("新增命令", on_click=lambda
            e: self.add_command_row())]))
        # self.command_rows.update()

    def build(self):
        result = Row([
            ElevatedButton("新增Tab", on_click=lambda e: self.add_tab_dialog())
        ], expand=True, vertical_alignment=CrossAxisAlignment.START)
        return result

    def update_dialog(self, is_open):
        self.dialog.open = is_open
        self.dialog.update()

    def add_tab_dialog(self):
        self.update_dialog(True)

    def create_tab(self):
        tab_name = self.tab_name_input.value
        if not tab_name:
            return
        scripts = []
        for row in self.command_rows.controls:
            title_input, cmd_input = row.controls  # 假设每一行都有两个控件
            if title_input.value and cmd_input.value:
                scripts.append({
                    "title": title_input.value,
                    "cmds": [cmd.strip() for cmd in cmd_input.value.split(',')]
                })

        new_content = {
            "tab_name": tab_name,
            "scripts": scripts
        }
        # 生成当前时间戳命名的文件
        timestamp = int(time.time())
        new_file_name = f"{timestamp}.json"
        new_file_path = os.path.join(curr_dir, "conf", new_file_name)
        # 创建新的JSON文件
        with open(new_file_path, "w", encoding="utf-8") as new_file:
            json.dump(new_content, new_file, indent=4, ensure_ascii=False)

        # 更新config.json
        config_path = os.path.join(curr_dir, "conf", "config.json")
        logging.debug(f"config_path:{config_path}")
        with open(config_path, "r", encoding="utf-8") as config_file:
            config = json.load(config_file)
        config["tabs"].append({"tab_name": tab_name, "conf_path": new_file_name})
        with open(config_path, "w", encoding="utf-8") as config_file:
            json.dump(config, config_file, indent=4, ensure_ascii=False)
        self.update_dialog(False)
        self.page.controls.clear()
        self.on_create_tab(self.page)
