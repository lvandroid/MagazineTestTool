import flet
from sidebar import Sidebar
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


class MainApp(UserControl):
    def build(self):

        return


def main(page: Page):
    page.title = "Magezine Test Tool"
    rail = Sidebar()
    page.add(Row([
        rail,
        VerticalDivider(width=1),
        IconButton(icon=icons.ARROW_BACK, on_click=lambda e: rail.hide()),
        Column([Text("Body!")], alignment=MainAxisAlignment.START, expand=True),
        VerticalDivider(width=1),
        Column([Text("Terminal...")], alignment=MainAxisAlignment.START, expand=True)
    ], expand=True))
    page.update()


flet.app(main)
