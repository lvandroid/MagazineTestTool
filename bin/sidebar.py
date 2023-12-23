from flet import (
    Page,
    UserControl,
    Column,
    Container,
    Row,
    Text,
    NavigationRail,
    NavigationRailDestination,
    NavigationRailLabelType,
    Icon,
    alignment,
    border_radius,
    colors,
    icons,
    padding,
    margin,
)


class Sidebar(UserControl):
    def build(self):
        self.bar = NavigationRail(
            visible=True,
            selected_index=0,
            label_type=NavigationRailLabelType.ALL,
            min_width=99,
            min_extended_width=399,
            group_alignment= -0.9,
            destinations=[
                NavigationRailDestination(icon=icons.DONE, selected_icon=icons.DONE_OUTLINE, label="外销", ),
                # NavigationRailDestination(icon_content=Icon(icons.UPGRADE_OUTLINED),
                                        #   selected_icon_content=Icon(icons.UPGRADE),
                                        #   label="自升级"),
                NavigationRailDestination(icon=icons.SETTINGS_OUTLINED,
                                          selected_icon_content=Icon(icons.SETTINGS),
                                          label_content=Text("设置"))
            ],
            on_change=lambda e: print("Selected destination:", e.control.selected_index),
        )
        return self.bar

    def hide(self):
        self.bar.visible = not self.bar.visible
        self.update()