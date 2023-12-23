import os, json, logging
from cmd import (
    execute_commands
)
from flet import (
    ElevatedButton,
)

def load_json_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)

# 获取当前脚本所在的目录
curr_dir = os.path.dirname(os.path.realpath(__file__))
# 构建JSON文件的路径
setting_json_file_path = os.path.join(curr_dir, "..", "conf", "settings.json")


def loading_settings(log_view, cmd_panel):
    if not os.path.exists(setting_json_file_path):
        logging.error("settings.json not exists")
        return {}
    with open(setting_json_file_path, "r", encoding="utf-8") as file:
        config = json.load(file)
        logging.debug(config)
        for item in config["adb_cmds"]:
            title = item["title"]
            cmds = item["cmds"]

            def on_click(e, cmd=cmds): execute_commands(cmds, log_view)

            cmd_panel.controls.append(ElevatedButton(text=title, on_click=lambda e: on_click(e)))
