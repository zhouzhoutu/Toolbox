from rope.base.simplify import real_code
import os,time,signal

def get_current_time():
    """获取当前时间并返回格式化的字符串"""
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

def set_focus_time():
    """提示用户设置专注时间并返回设置的时间（分钟）"""
    while True:
        try:
            pomotime = int(input("请输入您想要专注的时间（分钟）："))
            content = input("请输入您想要专注的内容：")
            if pomotime <= 0:
                raise ValueError("专注时间必须大于0分钟")
            print(f"您接下来将专注{pomotime}分钟，用于>>{content}<<，让我们开始吧！你目前的进度是：")
            return pomotime,content
        except ValueError:
            print("请输入有效的整数时间")

def handle_exit(signum, frame):
    """处理退出信号"""
    print("\n检测到退出信号，正在保存专注记录...")
    raise KeyboardInterrupt

def show_progress_bar(total_time):
    """显示进度条，支持提前退出和无限超时
    返回实际专注的分钟数
    """
    # 设置信号处理
    signal.signal(signal.SIGINT, handle_exit)

    start_minutes = 0
    progress = '⭕️' * total_time
    print(progress, end='\r')

    try:
        # 计时循环，去掉 <= total_time 的限制
        while True:
            time.sleep(60)  # 每分钟更新一次
            start_minutes += 1

            # 更新进度条
            if start_minutes <= total_time:
                progress = '✅' * start_minutes + '⭕️' * (total_time - start_minutes)
                print(f"{progress} ({start_minutes}/{total_time}分钟)", end='\r')
            elif start_minutes > total_time:
                # 超出预定时间的情况
                progress = '✅' * total_time + '⭐️' * (start_minutes - total_time)
                print(f"{progress} ({start_minutes}/{total_time}分钟)", end='\r')

    except KeyboardInterrupt:
        print(f"\n提前结束专注！实际专注了{start_minutes}分钟")

    return start_minutes

def get_focus_con():
    """提示用户输入专注感想（可选）"""

    content = input("请输入您实际做了什么：")
    feel = input("请输入您的专注感想,bad/ok/good!（可选）：")
    if feel:
        return content,feel
    else:
        return content,"无"

def save_to_file(start_time, end_time, focus_time, focus_content,real_content,focus_feel):
    """将专注信息保存到本地文件"""
    file_path = "pomotodo_log.csv"
    file_exists = os.path.exists(file_path)
    with open(file_path,"a",encoding='utf-8') as file:
        if not file_exists:
            file.write("开始时间,结束时间,专注时间,计划专注内容,实际做了什么,感想\n")
        # 写入数据行
        file.write(f"{start_time},{end_time},{focus_time},{focus_content},{real_content},{focus_feel}\n")

def main():
    start_time = get_current_time()
    print(f"现在时间是北京时间: {start_time}, 准备好一场专注之旅了嘛？(Y/n) ")
    if input().lower() != 'y':
        print("好的，下次再专注吧！")
        return

    focus_time, focus_content = set_focus_time()
    actual_time = show_progress_bar(focus_time)  # 获取实际专注时间
    end_time = get_current_time()
    real_con,focus_feel = get_focus_con()
    save_to_file(start_time, end_time, actual_time, focus_content,real_con, focus_feel)  # 保存实际专注时间
    print("专注信息已保存到pomotodo_log.csv文件中。")

if __name__ == "__main__":
    main()
