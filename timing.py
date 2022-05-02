from atexit import register
from datetime import datetime
from sys import modules
from time import (
    perf_counter_ns,
    time,
)

TIME_FORMAT = "%Y-%m-%d %H:%M:%S"


class TimeNs:
    def __init__(self, seconds, nanoseconds=0):
        """Constructor for TimeNs."""
        self.seconds = seconds
        self.nanoseconds = nanoseconds

    def __str__(self):
        return f"{int(self.seconds)}.{self.nanoseconds:09}"

    @property
    def time_as_int(self):
        return self.seconds * 10**9 + self.nanoseconds

    @property
    def time_as_float(self):
        return self.seconds + self.nanoseconds / 10**9


class Timing:
    lines = "=" * 30

    def __init__(self):
        """Constructor for Timing"""
        self.start_time = time()
        self.start_perf_counter = perf_counter_ns()

    def log(self, message, elapsed_time=None):
        print()
        print(Timing.lines)
        print(self.time_to_str() + ":", message)
        if elapsed_time is None:
            elapsed_time = self.time_elapsed
        print("Elapsed time:", elapsed_time, "ns")
        print(Timing.lines)

    def time_to_str(self):
        # TODO get str for a specific time?
        dt = datetime.fromtimestamp(self.current_time.seconds)
        return f"{dt.strftime(TIME_FORMAT)}.{self.current_time.nanoseconds:09}"

    @property
    def current_time(self):
        return TimeNs(seconds=time(), nanoseconds=perf_counter_ns())

    @property
    def time_elapsed(self):
        return TimeNs(
            seconds=self.seconds_elapsed, nanoseconds=self.nanoseconds_elapsed
        )

    @property
    def nanoseconds_elapsed(self):
        return perf_counter_ns() - self.start_perf_counter

    @property
    def seconds_elapsed(self):
        return time() - self.start_time


def test_module():
    timer = Timing()
    print(timer.time_to_str())
    timer.log("comecei o programa")
    print("teste\n" * 3)
    timer.log("printei varios testes")
    for _ in range(10**5):
        print(".", end="")
    timer.log("printei pontos na tela")
    timer.log("teste do elapsed_time", elapsed_time=10)


if __name__ == "__main__":
    test_module()


def end_log():
    timer.log(message=f"Program {calling_module} ended")


calling_module = modules["__main__"].__file__
timer = Timing()
timer.log(message=f"Program {calling_module} started")
register(end_log)
