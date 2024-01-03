from flet import (app, Page, FilePicker, Column, ElevatedButton, GridView, Row, Checkbox, Text, FilePickerResultEvent,
                  icons, TextField, UserControl, Container, ListView)

import pandas as pd
import logging

# 设置日志格式和级别
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# 调用过滤函数并传入列标题子字符串和过滤值
column_title_substring = '所属小组'
filter_value = '商业化应用一组'


def load_excel(file_path, operations_area: Column):
    global df
    df = pd.read_excel(file_path, sheet_name="BUG详情表")
    operations_area.controls.clear()
    for col in df.columns:
        chk = Checkbox(label=col, value=False)
        operations_area.controls.append(chk)
    operations_area.update()


def filter_dataframe():
    try:
        # 使用 filter 方法过滤列标题
        filtered_columns = df.filter(like=column_title_substring, axis=1)
        # 获取包含特定值的列的名称
        columns_to_filter = filtered_columns.columns
        # 构建包含多个条件的布尔索引
        conditions = [df[col].str.contains(filter_value, case=False, na=False) for col in columns_to_filter]
        combined_condition = any(conditions)
        # 使用布尔索引来过滤数据
        filtered_df = df[combined_condition]
        return filtered_df
    except Exception as e:
        logging.error(f"Error during filtering: {e}")
        return None


# 定义过滤函数
def filter_by_column_title_contains(dataframe, column_title_substring, filter_value):
    try:
        # 找到包含指定子字符串的列标题
        matching_columns = [col for col in dataframe.columns if column_title_substring in col]

        # 创建空的布尔索引
        filter_condition = None

        # 使用循环构建多个条件
        for col in matching_columns:
            condition = dataframe[col].str.contains(filter_value, case=False, na=False)
            if filter_condition is None:
                filter_condition = condition
            else:
                filter_condition = filter_condition | condition

        # 使用布尔索引来过滤数据
        filtered_df = dataframe[filter_condition]
        return filtered_df
    except Exception as e:
        print(f"Error during filtering: {e}")
        return None


# 过滤数据
def filter_data(operations_area: Column, details_area: TextField):
    data = filter_by_column_title_contains(df, column_title_substring, filter_value)
    # details_area.controls.clear()
    details_area.clean()
    select_columns = ["处理人", "所属项目", "[编号]标题", "当前状态", "优先级"]
    if data is not None:
        final_result = data.loc[:, select_columns]
        for index, row in final_result.iterrows():
            # details_area.controls.append(Text(row.values))
            details_area.value = details_area.value + row.values
            logging.debug(row.values)
        details_area.update()


class ExcelFilter(UserControl):
    def __init__(self, visible):
        super().__init__()
        self.visible = visible

    def build(self):
        self.filter_datas = [Text("1"), Text("2"), Text("3"), Text("4"), Text("5"), Text("6")]
        self.filter_list = ListView(controls=self.filter_datas, width=300)
        return Column([
            Row([
                ElevatedButton(
                    "请选择excel文件",
                ),
                # on_click=lambda _: pick_files_dialog.pick_files(
                #     allow_multiple=True, allowed_extensions=["xls", "xlsx"]
                # )),
                ElevatedButton("生成过滤后的数据",
                               # on_click=lambda _: filter_data(operations_area, details_area)
                               )
            ], expand=False),

            self.filter_list,
        ],
            expand=False)


def main(page: Page):
    def pick_files_result(e: FilePickerResultEvent):
        # selected_files.value = (
        #     ", ".join(map(lambda f: f.name, e.files)) if e.files else "Cancelled!"
        # )
        # selected_files.update()
        if e.files:
            load_excel(e.files[0].path, operations_area)

    pick_files_dialog = FilePicker(on_result=pick_files_result)
    # selected_files = Text()
    operations_area = Column(width=200, height=800, scroll=True)
    # details_area = Column(width=800)
    details_area = TextField()

    page.overlay.append(pick_files_dialog)

    page.add(
        Row(
            [
                Column([
                    ElevatedButton(
                        "Pick files",
                        icon=icons.UPLOAD_FILE,
                        on_click=lambda _: pick_files_dialog.pick_files(
                            allow_multiple=True, allowed_extensions=["xls", "xlsx"]
                        )),
                    ElevatedButton("生成过滤后的数据", on_click=lambda _: filter_data(operations_area, details_area))
                ],
                ),
                # selected_files,
                operations_area,
                details_area
            ]
        )
    )

# app(target=main)
