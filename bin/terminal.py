from flet import (
    UserControl,
    Column,
    Row,
    Text,
    ElevatedButton,
    Container,
    MainAxisAlignment,
    Markdown,
    MarkdownExtensionSet,
    Divider,
    Slider,
    colors
)


class Terminal(UserControl):

    def build(self):
        self.log_container = Markdown(
                                      auto_follow_links=True,
                                      extension_set=MarkdownExtensionSet.GITHUB_FLAVORED)
        self.terminal = Column(
            [
                Row([ElevatedButton(text="清空日志", on_click=lambda e: self.cleanLog()),
                     ElevatedButton(text="开始打印log",
                                    on_click=lambda e: self.appendLog(
                                        f"adb shell logcat|grep _V_MS-"),
                                    )
                     ]),
                Divider(height=1),
                Container(self.log_container, expand=True)
            ],
            alignment=MainAxisAlignment.START,
            expand=True)
        self.expand = True
        return self.terminal

    def cleanLog(self):
        print("clean log")
        self.log_container.value = ""
        self.log_container.update()

    def appendLog(self, log):
        self.log_container.value = f"```{self.log_container.value}\n{log}"
        self.log_container.update()
