import flet

from terminal import Terminal
from testspace import TestSpace
from settings import Settings
from flet import (
    Column,
    Row,
    NavigationRail,
    NavigationRailDestination,
    NavigationRailLabelType,
    Text,
    Page,
    Icon,
    VerticalDivider,
    icons,
    MainAxisAlignment,
    ThemeMode
)

import os
import logging

# 设置日志格式和级别
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


def add_adb_to_path():
    # 设置ADB的相对路径（根据您的实际路径调整）
    adb_path = os.path.abspath(os.path.join(".", "adb"))

    # 获取当前的PATH环境变量
    current_path = os.environ.get('PATH', '')

    # 将ADB路径添加到PATH环境变量
    if adb_path not in current_path:
        os.environ['PATH'] = adb_path + os.pathsep + current_path

    # 可以打印看看PATH环境变量是否已经被正确修改
    logging.info(os.environ['PATH'])


terminal = Terminal()
# 主体内容区域
body_content = Column([], alignment=MainAxisAlignment.START, expand=True)
# 创建页面内容视图
content_views = [
    Row([
        # IconButton(icon=icons.ARROW_BACK, on_click=lambda e: rail.hide(),width=5),
        VerticalDivider(width=1),
        TestSpace(width=300),
        # Column([], alignment=MainAxisAlignment.START, width=300, expand=False),
        VerticalDivider(width=1),
        terminal,
    ], expand=True),
    Column([Text("自升级")]),  # 第二页内容
    Settings(),
]


# 更新页面内容的函数
def update_content(index):
    body_content.controls.clear()
    content = content_views[index]
    body_content.controls.append(content)
    body_content.update()
    if isinstance(content, Settings):
        content.loading_settings()


# 导航栏变化时的回调函数
def on_nav_change(e):
    update_content(e.control.selected_index)


def appLayout():
    rail = NavigationRail(
        visible=True,
        selected_index=0,
        label_type=NavigationRailLabelType.ALL,
        min_width=99,
        min_extended_width=399,
        group_alignment=-0.9,
        destinations=[
            NavigationRailDestination(icon=icons.DONE, selected_icon=icons.DONE_OUTLINE, label="外销", ),
            NavigationRailDestination(icon_content=Icon(icons.UPGRADE_OUTLINED),
                                      selected_icon_content=Icon(icons.UPGRADE), label="自升级"),
            NavigationRailDestination(icon=icons.SETTINGS_OUTLINED,
                                      selected_icon_content=Icon(icons.SETTINGS),
                                      label_content=Text("设置"))
        ],
        on_change=on_nav_change
    )
    return Row([
        rail,
        VerticalDivider(width=1),
        body_content,
    ], expand=True)


def main(page: Page):
    add_adb_to_path()
    page.title = "阅图测试工具"
    page.theme_mode = ThemeMode.SYSTEM
    page.auto_scroll = True
    page.add(appLayout())
    update_content(0)
    page.update()


flet.app(main)