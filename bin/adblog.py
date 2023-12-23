import subprocess
import threading
import datetime

# 创建一个全局变量用于存储之前的线程
previous_thread = None


def read_logcat(tags=None, log_view=None):
    try:
        # 启动adb logcat命令
        logcat_process = subprocess.Popen(['adb', 'logcat'], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                          stdin=subprocess.PIPE, universal_newlines=True, encoding='utf-8')

        # 创建一个线程来实时读取logcat输出
        def logcat_reader():
            while True:
                line = logcat_process.stdout.readline()
                if not line:
                    break
                if tags:
                    for tag in tags:
                        if tag in line:
                            print_log(line.strip(), log_view)
                            break
                else:
                    print_log(line.strip(), log_view)

        # 启动线程来读取日志
        logcat_thread = threading.Thread(target=logcat_reader)
        logcat_thread.start()

        # 等待线程结束
        logcat_thread.join()

    except KeyboardInterrupt:
        # 捕获Ctrl+C中断，关闭logcat进程
        logcat_process.terminate()
        logcat_thread.join()


def print_log(log, log_view):
    if log_view != None:
        log_view.value += f"{log}\n"
        log_view.update()
    else:
        print(log)


def clear_logcat_cache():
    try:
        # 执行adb logcat -c命令以清除logcat缓存
        subprocess.run(['adb', 'logcat', '-c'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE,
                       creationflags=subprocess.CREATE_NO_WINDOW)
    except Exception as e:
        print(f"Error clearing logcat cache: {e}")


# def _log_to_file(log): # 保存文件到文件中
#     # 获取当前日期作为文件名的一部分
#     current_date = datetime.datetime.now().strftime("%Y-%m-%d")
#     # 构建文件名，例如：2023-12-07.log
#     log_file= f"{current_date}.log"
#     if log_file:
#         with open(log_file, 'a') as file:
#             file.write(log + '\n')

def write_log_to_file(log_tuple):
    log_str, = log_tuple  # 解包元组，获取 log_str
    # 指定要过滤的TAG字符串，以列表形式传递
    tags_to_filter = ['_V_MS-', ]

    # 获取当前日期作为文件名的一部分
    current_date = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    # 构建文件名，例如：2023-12-07.log
    log_file_name = f"{current_date}.log"

    # 过滤日志，将满足条件的日志写入文件
    if any(tag in log_str for tag in tags_to_filter):
        log_to_file(log_str, log_file_name)


def log_to_file(log, log_file):
    if log_file:
        with open(log_file, 'a') as file:
            file.write(log + '\n')


def magazine_log_to_file(log_str):
    threading.Thread(target=write_log_to_file, args=((log_str,),), daemon=True).start()


def default_magazine_log(logview):
    tags_to_filter = ['_V_MS-', ]
    log_by_tag(logview, tags_to_filter)


def log_by_tag(logview, tags):
    global previous_thread  # 声明全局的previous_thread

    print(f"log_by_tag{tags}")
    clear_logcat_cache()
    # 中断之前的线程
    if previous_thread:
        previous_thread.join()

    # 创建一个新线程并保存到previous_thread
    previous_thread = threading.Thread(target=read_logcat, args=(tags, logview), daemon=True)
    previous_thread.start()