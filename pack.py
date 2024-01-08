from utils import exec_cmd
import logging, subprocess, os
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
# 获取当前脚本所在的目录
current_dir = os.path.dirname(os.path.abspath(__file__))
logo = os.path.join(current_dir, "assets", "icon_1.png")

# 使用相对路径引用 work_tools.py 文件
work_tools_script = os.path.join(current_dir, "work_tools.py")
pack_cmd = [f"flet pack -i {logo} -n 常用工具 {work_tools_script}"]

if __name__ == '__main__':
    exec_cmd(pack_cmd)