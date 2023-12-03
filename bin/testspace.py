from flet import (
    UserControl,
    Column,
    Row,
    Text,
    OutlinedButton,
    Container,
    MainAxisAlignment,
    Markdown,
    MarkdownExtensionSet,
    Divider,
    Slider,
    margin,
    GridView,
    colors
)


class TestSpace(UserControl):
    def build(self):
        return GridView(
            [
                OutlinedButton(text="重新挂载"),
                OutlinedButton(text="ROOT手机"),
                OutlinedButton(text="切换测试环境"),
                OutlinedButton(text="切换正式环境"),
                OutlinedButton(text="清除阅图数据"),
            ],
            runs_count=2,
            child_aspect_ratio=4,
            run_spacing=30,

        )
