import flet
from sidebar import Sidebar
from terminal import Terminal
from testspace import TestSpace
from flet import (
    UserControl,
    TextField,
    ElevatedButton,
    TextButton,
    Container,
    Column,
    Row,
    ResponsiveRow,
    NavigationRail,
    NavigationRailDestination,
    NavigationRailLabelType,
    FloatingActionButton,
    Image,
    Text,
    Page,
    Icon,
    IconButton,
    VerticalDivider,
    icons,
    colors,
    MainAxisAlignment,
    theme
)


def appLayout():
    rail = Sidebar()
    terminal = Terminal()
    return Row([
        rail,
        IconButton(icon=icons.ARROW_BACK_SHARP, on_click=lambda e: rail.hide(),width=5),
        VerticalDivider(width=1),
        TestSpace(width= 300),
        # Column([], alignment=MainAxisAlignment.START, width=300, expand=False),
        VerticalDivider(width=1),
        terminal,
    ], expand=True)


def main(page: Page):
    page.title = "阅图测试工具"
    page.add(appLayout())
    page.update()


flet.app(main)
