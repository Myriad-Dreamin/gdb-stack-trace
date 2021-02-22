
# insert root directory
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.absolute()))

from wrap_gdb import gdb_ins
import os
import re
import subprocess

# settings
gdb_ins.set_log("gdb.log")
gdb_ins.set_logging_redirect(False)
gdb_ins.set_logging(True)

# todo thread-events
gdb_ins.execute("set print thread-events off")
gdb_ins.execute("set pagination off")
gdb_ins.execute("set confirm off")

gdb = gdb_ins.process

yellow = '\033[1;33m'
cyan = '\033[1;36m'
reset_color = '\033[0;0m'

class FunctionEnterBreakpoint(gdb.Breakpoint):
    def __init__(self, spec, runner):
        self._function_name = spec
        self.runner = runner
        super(FunctionEnterBreakpoint, self).__init__(spec, internal=True)

    @staticmethod
    def stack_depth():
        depth = -1
        frame = gdb.newest_frame()
        while frame:
            frame = frame.older()
            depth += 1
        return depth

    def stop(self):
        info_args = gdb.execute(
            'info args', from_tty=False, to_string=True)
        if info_args == 'No arguments.\n':
            args_str = ''
        else:
            args_str = ', '.join(info_args.splitlines())
        self.runner.write_trace(
            f"{'  ' * (self.stack_depth())}{cyan}{self._function_name}{reset_color} ({args_str})")
        return False  # continue immediately


class TestCaseRunner(object):

    def __init__(self):
        self.tracing_function = []
        self.trace_msg_list = []
    
    def write_trace(self, msg):
        self.trace_msg_list.append(msg)

    def stop_handler(self, event):
        gdb_ins.execute("set scheduler-locking on") # to avoid parallel signals in other threads
        stop_signal = getattr(event, 'stop_signal')
        if stop_signal is None:
            return

        print(f"{cyan}[exited] SIG {stop_signal}{reset_color}")

    def trace_functions(self, fs):
        self.tracing_function.extend(fs)
        for f in fs:
            FunctionEnterBreakpoint(f, self)

    def run(self, file=None):
        print(f"{cyan}>>> beg collecting of test case {yellow}{file}{cyan}...{reset_color}")
        
        p = Path(f"{file}.out")
        p.parent.mkdir(parents=True, exist_ok=True)
        
        gdb_ins.execute(f"set environment KTEST_FILE={file}")
        print(f"{cyan} >>> beg execution{reset_color}")
        gdb_ins.run(stdin=file, stdout=p)
        print(f"{cyan} <<< end execution{reset_color}")
        
        trace = '\n'.join(self.trace_msg_list)
        if 'kbase_open' in trace:
            idx = trace.find('kbase_open')
            assert idx != -1
            while trace[idx] != '\n':
                idx-=1
            trace = trace[idx:]
            while trace[1] == ' ':
                trace = trace.replace('\n  ', '\n')
            print(trace[1:])
        else:
            print(trace)

        print(f"{cyan}<<< end collecting of test case...{reset_color}")

tcr = TestCaseRunner()
gdb_ins.process.events.stop.connect(tcr.stop_handler)

interestring_obj_types = ['T'] # + ['t']
functions = dict(map(lambda ft: (ft, []), interestring_obj_types))


binary_path = 'build/test-main'

for matched in re.finditer(
    r'[\da-f]+\s+(\S+)\s+(\S+)\n',
    subprocess.check_output(['nm', binary_path]).decode('utf8')
):
    symbol_type, function = matched[1], matched[2]

    if symbol_type in functions:
        functions[symbol_type].append(function)

print('\n'.join([f'{k}:{v}' for k, v in functions.items()]))
functions = set(sum(functions.values(), []))
print(len(functions))

tcr.trace_functions(list(functions))
tcr.run()
