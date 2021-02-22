
# insert root directory
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.absolute()))

import gdb # pylint: disable=all
import os
import re
import subprocess

# todo thread-events
gdb.execute("set print thread-events off")
gdb.execute("set pagination off")
gdb.execute("set confirm off")

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
        bt = gdb.execute('backtrace 1', from_tty=False, to_string=True)[len('#0  '):].split(' at ')[0].strip()
        self.runner.write_trace(f"{'  ' * (self.stack_depth())}{bt}")
        return False  # continue immediately

class TestCaseRunner(object):

    def __init__(self):
        self.trace_msg_list = []
        self.print_lines = []
    
    def write_trace(self, msg):
        self.trace_msg_list.append(msg)

    def trace_functions(self, fs):
        for f in fs:
            FunctionEnterBreakpoint(f, self)

    def run(self, file=None):
        args = ""
        if file:
            args += f"< {file}"
        gdb.execute(f"set args {args} > {file}.out")
        gdb.execute("run")
        print('\n'.join(["=" * 120] + self.print_lines + self.trace_msg_list))

tcr = TestCaseRunner()

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
        if not i_regex.search(function):
            continue

    if symbol_type in functions:
        functions[symbol_type].append(function)

tcr.trace_functions(list(set(sum(functions.values(), []))))
tcr.run()
