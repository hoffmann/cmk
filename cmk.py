def fmt_perf(data):
    if len(data) < 2 or len(data) > 6:
        raise ValueError("data must have between 2 and 5 fields")
    
    return "%s=%s" %(data[0], ";".join(map(str, data[1:])))

class Check(object):
    OK = 0
    WARNING = 1
    CRITICAL = 2
    UNKNOWN = 3
    COMPUTE_PERF = 'P'

    def __init__(self, name):
        self.name = name

    def format(self, status, message, performance_data=None):
        if performance_data is None:
            perf = "-"
        else:
            perf = "|".join(fmt_perf(data) for data in performance_data)
        return "%s %s %s %s" %(status, self.name, perf, message)

    def ok(self, msg, perf=None):
        return self.format(self.OK, msg, perf) 

    def warn(self, msg, perf=None):
        return self.format(self.WARNING, msg, perf) 

    def crit(self, msg, perf=None):
        return self.format(self.CRITICAL, msg, perf) 

    def unknown(self, msg, perf=None):
        return self.format(self.UNKNOWN, msg, perf) 

    def compute(self, msg, perf):
        return self.format(self.COMPUTE_PERF, msg, perf) 
