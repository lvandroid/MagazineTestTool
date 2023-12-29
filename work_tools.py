import os, json, logging

import flet, subprocess, shlex
from bin.settings import Settings
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


def exec_cmd(cmd, log_view: TextField):
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    # creationflags=subprocess.CREATE_NO_WINDOW)
    # 获取标准输出和标准错误
    stdout_output = result.stdout
    stderr_output = result.stderr

    # 检查命令是否成功执行
    if result.returncode == 0:
        # 打印标准输出
        log_view.value = f"{log_view.value}\n{stdout_output}"
    else:
        # 如果命令执行失败，可以打印错误信息
        log_view.value = f"{log_view.value}\n{stderr_output}"
    log_view.scroll_to = len(log_view.value)
    log_view.update()


def execute_commands(cmds, log_view):
    for cmd in cmds:
        c = shlex.split(cmd)
        log_view.value = f"{log_view.value}\n{cmd}"
        log_view.update()
        exec_cmd(c, log_view)


def clean_log(self):
    self.log_view.value = ""
    self.log_view.update()


def main(page: Page):
    cmd_panel = Column(width=200, expand=False)
    terminal = TextField("", text_size=12, height=600, expand=True, multiline=True, read_only=True,
                         autofocus=True)

    def load_json_file(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)

    # 获取当前脚本所在的目录
    curr_dir = os.path.dirname(os.path.realpath(__file__))
    # 构建JSON文件的路径
    config_path = os.path.join(curr_dir, "conf", "config.json")
    config = load_json_file(config_path)
    logging.debug(config)

    def create_button_with_cmd(title, cmd_array):
        def on_click(e):
            execute_commands(cmd_array, terminal)

        return ElevatedButton(text=title, on_click=on_click)

    # 根据配置文件加载对应的脚本命令
    def load_scripts(conf_path):
        full_path = os.path.join(curr_dir, "conf", conf_path)
        scripts_config = load_json_file(full_path)
        cmd_panel.controls.clear()
        for script in scripts_config["scripts"]:
            logging.debug(f"script:{script}")
            title = script["title"]
            cmds = script["cmds"]

            cmd_panel.controls.append(create_button_with_cmd(title, cmds))

    destinations = []
    conf_path = []
    for tab in config["tabs"]:
        tab_name = tab["tab_name"]
        conf_path.append(tab["conf_path"])
        destinations.append(NavigationRailDestination(label=tab_name, icon=icons.LABEL))
        logging.debug(f"tab:{tab}")
    destinations.append(NavigationRailDestination(label="设置", icon=icons.SETTINGS))

    navigator = NavigationRail(visible=True,
                               selected_index=0,
                               label_type=NavigationRailLabelType.ALL,
                               min_width=99,
                               min_extended_width=399,
                               group_alignment=-0.9,
                               destinations=destinations,
                               )

    def on_nav_change(e):
        panel_visible = e.control.selected_index != len(conf_path)
        if panel_visible:
            load_scripts(conf_path[e.control.selected_index])
        update_view(panel_visible)
        navigator.destinations = destinations
        navigator.update()
        cmd_panel.update()

    setting_page = Settings(visible=False)

    def update_view(cmd_panel_visible):
        if cmd_panel_visible:
            cmd_panel.visible = True
            terminal.visible = True
            setting_page.visible = False
        else:
            cmd_panel.visible = False
            terminal.visible = False
            setting_page.visible = True
        page.update()

    navigator.on_change = on_nav_change
    load_scripts(conf_path[0])
    page.add(Row([
        navigator,
        VerticalDivider(width=1),
        cmd_panel,
        VerticalDivider(width=1),
        terminal,
        setting_page
    ], expand=True))
    cmd_panel.update()
    page.update()


flet.app(target=main)