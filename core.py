
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

cpp_fn_mapping = dict()

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
        bt = gdb.execute('backtrace 1', from_tty=False, to_string=True)[len('#0  '):].split(' at ')[0].strip()
        mapping = cpp_fn_mapping.get(self._function_name)
        if mapping:
            # self.runner.print(f'cpp_fn_mapping is {self._function_name} => {mapping}')
            finds = re.search(f"{mapping['method']} \(", bt)
            span = finds.span()
            # self.runner.print(f"""search: {repr(finds.span())}""")
            self.runner.write_trace(
                f"{'  ' * (self.stack_depth())}{yellow}{mapping['cls']}{reset_color}::{cyan}{mapping['method']}{reset_color}{bt[span[0]+len(mapping['method']):]}")
        else:
            a = bt.find('(')
            if a != -1:
                self.runner.write_trace(
                    f"{'  ' * (self.stack_depth())}{cyan}{bt[:a]}{reset_color}{bt[a:]}")
            else:
                self.runner.write_trace(
                    f"{'  ' * (self.stack_depth())}{bt}")
        return False  # continue immediately

class TestCaseRunner(object):

    def __init__(self):
        self.trace_msg_list = []
        self.print_lines = []
    
    def write_trace(self, msg):
        self.trace_msg_list.append(msg)

    def stop_handler(self, event):
        gdb_ins.execute("set scheduler-locking on") # to avoid parallel signals in other threads
        stop_signal = getattr(event, 'stop_signal')
        if stop_signal is None:
            return

        print(f"{cyan}[exited] SIG {stop_signal}{reset_color}")
    
    def print(self, line):
        self.print_lines.append(line)

    def trace_functions(self, fs):
        for f in fs:
            FunctionEnterBreakpoint(f, self)

    def run(self, file=None):
        print(f"{cyan}>>> beg collecting of test case {yellow}{file}{cyan}...{reset_color}")
        
        p = Path(f"{file}.out")
        p.parent.mkdir(parents=True, exist_ok=True)
        
        print(f"{cyan} >>> beg execution{reset_color}")
        gdb_ins.run(stdin=file, stdout=p)
        print(f"{cyan} <<< end execution{reset_color}")
        print('\n'.join(self.print_lines))
        print('\n'.join(self.trace_msg_list))
        print(f"{cyan}<<< end collecting of test case...{reset_color}")

tcr = TestCaseRunner()
gdb_ins.process.events.stop.connect(tcr.stop_handler)

interestring_obj_types = ['T', 'W'] # + ['t']
functions = dict(map(lambda ft: (ft, []), interestring_obj_types))

binary_path = 'build/test-main'

gen_regex_list = lambda _cls: lambda _method: f'(?P<cls>{_cls}).*(?P<method>{_method})'

regexes = []

# 'vector.*'
regexes.append(gen_regex_list('vector')('|'.join(['push_back'])))

i_regex = re.compile('|'.join(map(lambda si: f'(?:{si})', regexes)))

for matched in re.finditer(
    r'[\da-f]+\s+(\S+)\s+(\S+)\n',
    subprocess.check_output(['nm', binary_path]).decode('utf8')
):
    symbol_type, function = matched[1], matched[2]
    
    if symbol_type == 'W':
        matched = i_regex.search(function)
        if not matched:
            continue
        cpp_fn_mapping[function] = matched.groupdict()

    if symbol_type in functions:
        functions[symbol_type].append(function)

print('\n'.join([f'{k}:{v}' for k, v in functions.items()]))
functions = set(sum(functions.values(), []))

tcr.trace_functions(list(functions))
tcr.run()
