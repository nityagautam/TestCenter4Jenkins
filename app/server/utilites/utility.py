import re


class Utility:
    def __init__(self):
        pass

    @staticmethod
    def covert_str_time_to_mins(str_time: str):
        calculated_time_in_mins = 0
        x = re.search("^[(\d*)\s*day]*\s*[(\d*)\s*hr]*\s*[(\d*)\s*min]*\s*$", str_time)
        if x:
            x_day = re.search("(\d+\s*[day]+)+", str_time)
            if x_day:
                x_day = x_day.groups()[0].split(" ")[0]
            else:
                x_day = 0

            x_hour = re.search("(\d+\s*[hr]+)+", str_time)
            if x_hour:
                x_hour = x_hour.groups()[0].split(" ")[0]
            else:
                x_hour = 0

            x_min = re.search("(\d+\s*[min]+)+", str_time)
            if x_min:
                x_min = x_min.groups()[0].split(" ")[0]
            else:
                x_min = 0

            calculated_time_in_mins = eval(f"({x_day}*60*24)+({x_hour}*60)+({x_min})")
            # print(x_day, x_hour, x_min)
            # print(f"Total time (in mins): {calculated_time_in_mins)}")

        return calculated_time_in_mins


# =======================================
# Decorator to handle the Exception
# =======================================
def global_exception(origin_func):
    def wrapper(self, *args, **kwargs):
        try:
            u = origin_func(self, *args, **kwargs)
            return u
        except Exception as e:
            print('[ERROR]: ', e)
            return '0'

    return wrapper