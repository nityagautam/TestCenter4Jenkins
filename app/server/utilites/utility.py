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

