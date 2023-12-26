import os, json, logging
from cmd import (
    execute_commands
)
from flet import (
    NavigationRail,
    NavigationRailDestination,
    ElevatedButton,
    UserControl,
    Row,
    Column,
    TextField,
    icons,
)


class CmdPanel(UserControl):
    def build(self):
        self.cmd_panel = Column(expand=True)
        self.terminal = TextField(width=200)
        self.navigation = NavigationRail()
        return Row([
            self.navigation,
            self.terminal,
            self.cmd_panel
        ], expand=True)

    def load_config(self):
        def load_json_file(file_path):
            with open(file_path, "r", encoding="utf-8") as file:
                return json.load(file)

        # 获取当前脚本所在的目录
        curr_dir = os.path.dirname(os.path.realpath(__file__))
        # 构建JSON文件的路径
        config_path = os.path.join(curr_dir, "..", "conf", "config.json")
        config = load_json_file(config_path)

        # 根据配置文件加载对应的脚本命令
        def load_scripts(conf_path):
            full_path = os.path.join(curr_dir, "..", "conf", conf_path)
            scripts_config = load_json_file(full_path)
            self.cmd_panel.controls.clear()

            for script in scripts_config["scripts"]:
                title = script["title"]
                cmds = script["cmds"]

                def on_click(e, cmd=cmds): execute_commands(cmds, self.cmd_panel)

                self.cmd_panel.controls.append(ElevatedButton(text=script["title"], on_click=lambda e: on_click(e)))
            self.cmd_panel.update()

            destinations = []
            for tab in config["tabs"]:
                tab_name = tab["tab_name"]
                conf_path = tab["conf_path"]

                def on_click(e, conf_path=conf_path):
                    load_scripts(conf_path)

                destinations.append(icons.FOLDER),
                on_click = on_click
            self.navigation.destinations=destinations
            self.navigation.update()

# def loading_settings(log_view, cmd_panel):
#     if not os.path.exists(config_path):
#         logging.error("settings.json not exists")
#         return {}
#     with open(config_path, "r", encoding="utf-8") as file:
#         config = json.load(file)
#         logging.debug(config)
#         for item in config["adb_cmds"]:
#             title = item["title"]
#             cmds = item["cmds"]
#
#             def on_click(e, cmd=cmds): execute_commands(cmds, log_view)
#
#             cmd_panel.controls.append(ElevatedButton(text=title, on_click=lambda e: on_click(e)))
