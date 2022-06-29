import time, os, sched

schedule = sched.scheduler(time.time, time.sleep)

python_cmd = ""
def perform_command(cmd, inc):
    schedule.enter(inc, 0, perform_command, (cmd, inc))
    os.system(cmd)


def timming_exe(cmd, inc=60 * 60 * 24):
    # enter从现在起第n秒开始运行
    schedule.enter(inc, 0, perform_command, (cmd, inc))
    # 运行结束
    schedule.run()
