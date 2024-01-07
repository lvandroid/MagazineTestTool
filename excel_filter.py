import flet
from flet import (app, Page, FilePicker, Column, ElevatedButton, GridView, Row, Checkbox, Text, FilePickerResultEvent,
                  icons, TextField, UserControl, Container, ListView)

import utils
import pandas as pd
import logging
import re

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
    details_area.clean()
    select_columns = ["处理人", "[编号]标题", ]
    if data is not None:
        final_result = data.loc[:, select_columns]
        for index, row in final_result.iterrows():
            row_str = ", ".join(map(str, row.values))
            details_area.value += row_str + "\n"
        details_area.update()


def filter_data_simple(operations_area: Column, details_area: TextField):
    data = filter_by_column_title_contains(df, column_title_substring, filter_value)
    details_area.value = ""  # 清除之前的内容
    result_dict = {}  # 创建一个字典来保存处理人和编号的对应关系

    select_columns = ["处理人", "所属项目", "[编号]标题", "优先级"]
    if data is not None:
        final_result = data.loc[:, select_columns]
        for index, row in final_result.iterrows():
            # 获取处理人
            person = row["处理人"]
            # 使用正则表达式提取方括号内的内容
            project_code = re.findall(r'\[([^\]]*)\]', row["[编号]标题"])
            project_code = project_code[0] if project_code else ""  # 获取第一个匹配项

            # 添加到字典中
            if person in result_dict:
                result_dict[person].add(f"[{project_code}]")  # 使用集合来避免重复
            else:
                result_dict[person] = {f"[{project_code}]"}

        # 格式化输出
        for person, codes in result_dict.items():
            codes_str = " ".join(codes)
            details_area.value += f"@{person} {codes_str}\n"  # 名字后换行

        details_area.update()


class ExcelFilter(UserControl):
    def __init__(self, visible, page):
        super().__init__()
        self.visible = visible
        self.page = page

    def build(self):
        self.filter_datas = [Text("1"), Text("2"), Text("3"), Text("4"), Text("5"), Text("6")]
        self.filter_list = ListView(controls=self.filter_datas, width=300)

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
        details_area = TextField(text_size=12, height=600, width=500, multiline=True, read_only=True,
                                 autofocus=True)

        self.page.overlay.append(pick_files_dialog)

        return Row(
            [
                Column([
                    ElevatedButton(
                        "请选择excel文件",
                        on_click=lambda _: pick_files_dialog.pick_files(
                            allow_multiple=True, allowed_extensions=["xls", "xlsx"]
                        )),
                    ElevatedButton("生成过滤后的数据",
                                   on_click=lambda _: filter_data_simple(operations_area, details_area))
                ],
                ),
                # selected_files,
                operations_area,
                details_area
            ]
        )
