import os, json, logging

import flet

from cmd import (
    execute_commands
)
from flet import (
    NavigationRail,
    NavigationRailDestination,
    NavigationRailLabelType,
    ElevatedButton,
    UserControl,
    Row,
    Column,
    TextField,
    icons,
    VerticalDivider,
    Page,
)

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


def main(page: Page):
    cmd_panel = Column(width=200, expand=False)
    terminal = TextField(hint_text="Terminal", width=200, expand=True)

    def load_json_file(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)

    # 获取当前脚本所在的目录
    curr_dir = os.path.dirname(os.path.realpath(__file__))
    # 构建JSON文件的路径
    config_path = os.path.join(curr_dir, "..", "conf", "config.json")
    config = load_json_file(config_path)
    logging.debug(config)

    # 根据配置文件加载对应的脚本命令
    def load_scripts(conf_path):
        full_path = os.path.join(curr_dir, "..", "conf", conf_path)
        scripts_config = load_json_file(full_path)
        cmd_panel.controls.clear()
        for script in scripts_config["scripts"]:
            logging.debug(f"script:{script}")
            title = script["title"]
            cmds = script["cmds"]

            def on_click(e, cmd=cmds): execute_commands(cmds, terminal)

            cmd_panel.controls.append(ElevatedButton(text=title, on_click=lambda e: on_click(e)))

    destinations = []
    conf_path = []
    for tab in config["tabs"]:
        tab_name = tab["tab_name"]
        conf_path.append(tab["conf_path"])
        destinations.append(NavigationRailDestination(label=tab_name, icon=icons.FOLDER))
        logging.debug(f"tab:{tab}")

    navigator = NavigationRail(visible=True,
                               selected_index=0,
                               label_type=NavigationRailLabelType.ALL,
                               min_width=99,
                               min_extended_width=399,
                               group_alignment=-0.9,
                               destinations=destinations,
                               )

    def on_nav_change(e):
        load_scripts(conf_path[e.control.selected_index])
        navigator.destinations = destinations
        navigator.update()
        cmd_panel.update()

    navigator.on_change = on_nav_change
    load_scripts(conf_path[0])
    page.add(Row([
        navigator,
        VerticalDivider(width=1),
        cmd_panel,
        VerticalDivider(width=1),
        terminal,
    ], expand=True))
    cmd_panel.update()
    page.update()


flet.app(target=main)