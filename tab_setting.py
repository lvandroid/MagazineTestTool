from flet import (
    UserControl,
    Column,
    Row,
    TextField,
    ElevatedButton,
    AlertDialog,
    TextButton,
    ListView,
)

import logging, time, os, json
import uuid

# 获取当前脚本所在的目录
curr_dir = os.path.dirname(os.path.realpath(__file__))


class TabSetting(UserControl):
    def __init__(self, page, on_create_tab):
        super().__init__()
        self.page = page
        self.on_create_tab = on_create_tab
        self.cmd_rows = {}  # 使用字典来存储命令行及其ID
        self.tab_name_input = TextField(label="Tab名称", hint_text="请输入tab的名称", autofocus=True, width=200)
        self.title_panel = Row([on_create_tab, self.add_cmd_btn()], expand=True)

        self.cmd_list = ListView(expand=1, spacing=10, auto_scroll=True, width=800, )
        self.dialog_content = Column([self.tab_name_input, self.add_cmd_btn(), self.cmd_list])
        self.add_command_row()  # 初始时添加一组命令输入框

        self.dialog = AlertDialog(
            content=self.dialog_content,
            actions=[
                ElevatedButton("确认", on_click=lambda e: self.create_tab()),
                TextButton("取消", on_click=lambda e: self.update_dialog(False))
            ],
        )
        self.page.dialog = self.dialog

    def add_cmd_btn(self):
        return ElevatedButton("新增命令", on_click=lambda e: self.add_refresh_row())

    def add_refresh_row(self):
        self.add_command_row()
        self.cmd_list.update()

    def delete_cmd(self, row_id):
        logging.debug(f"delete row_id:{row_id}")
        if row_id in self.cmd_rows:
            self.cmd_list.controls.remove(self.cmd_rows[row_id])
            del self.cmd_rows[row_id]
            logging.debug(f"delete row_id:{row_id}")
            self.cmd_list.update()

    def add_command_row(self):
        row_id = str(uuid.uuid4())  # 生成一个唯一的ID
        # 创建新的命令输入框
        title_input = TextField(label="标题", hint_text="请输入命令标题", width=200)
        cmd_input = TextField(label="命令", hint_text="请输入命令，多个命令用逗号隔开", width=400)
        del_btn = TextButton("删除", on_click=lambda e: self.delete_cmd(row_id))
        cmd_item = Row([title_input, cmd_input, del_btn], width=600)
        self.cmd_rows[row_id] = cmd_item
        self.cmd_list.controls.append(cmd_item)
        logging.debug(f"add row_id:{row_id}")

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
        for row in self.cmd_rows.values():
            if len(row.controls) >= 2:
                title_input = row.controls[0]
                cmd_input = row.controls[1]
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

    def build(self):
        return Column([
            Row([
                ElevatedButton("创建Tab", on_click=lambda _: self.add_tab_dialog())
            ])
        ], expand=True)
