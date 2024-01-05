from flet import (
    Page, SnackBar, Text,
)


def show_toast(page: Page, msg):
    snack_bar = SnackBar(content=Text(msg), duration=1000)
    page.snack_bar = snack_bar
    page.snack_bar.open = True
    page.update()
