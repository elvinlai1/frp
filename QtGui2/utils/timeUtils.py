from datetime import datetime
import math


def time_format(times=None, format="%Y-%m-%d %H:%M:%S"):
    if times:
        return datetime.strptime(times, format).strftime(format)
    else:
        return datetime.now().strftime(format)


def secondsToHours(seconds):
    # calculate day difference
    days = math.floor(seconds / (24 * 3600 * 1000))

    # calculate hours
    leave1 = seconds % (24 * 3600 * 1000)
    hours = math.floor(leave1 / (3600 * 1000))

    # calculate minutes
    leave2 = leave1 % (3600 * 1000)
    minutes = math.floor(leave2 / (60 * 1000))

    # calculate seconds
    leave3 = leave2 % (60 * 1000)
    second = round(leave3 / 1000)
    return days, hours, minutes, second


def check_timestamp(pre_time_s, next_time_s=datetime.now()):
    pre_date = time_format(format='%Y-%m-%d')
    n_times = next_time_s.timestamp()
    current_timer = f'{pre_date} {pre_time_s}'
    p_times = datetime.strptime(current_timer, "%Y-%m-%d %H:%M:%S").timestamp()
    print(f'{n_times - p_times} ===> {next_time_s.strftime("%Y-%m-%d %H:%M:%S")} ===> {current_timer}')
    return (n_times - p_times) * 1000


if __name__ == '__main__':
    pass
    # print(datetime.now().strftime('%H-%M-%S', ))
    # b = datetime(2022, 2, 19, 16, 20, 20)
    # sec = (datetime.now() - b).seconds
    # print(datetime.strptime('2022-02-19 09:05:03', "%Y-%m-%d %H:%M:%S").timestamp())
    # timers = datetime.now().timestamp() - datetime.strptime('2022-02-19 09:05:03', "%Y-%m-%d %H:%M:%S").timestamp()
    # print(secondsToHours(timers * 1000))
    # print((datetime.now() - datetime.strptime('2022-02-19 09:05:03',"%Y-%m-%d %H:%M:%S").second))
    # print(secondsToHours(sec * 1000))
    # print(datetime.date())
