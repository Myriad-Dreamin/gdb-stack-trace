
import gdb as gdb_process # pylint: disable=all

class GDBInstance(object):
    process: object

    def __init__(self):
        """
        configuration
        """

        self.process = gdb_process
    
    def execute(self, cmd, to_string=True):
        return self.process.execute(cmd, to_string=to_string)
    
    def set_log(self, log_file_path):
        return self.execute(f"set logging file {log_file_path}")
    
    def set_logging(self, on=False):
        return self.execute(f"set logging {'on' if on else 'off'}")
    
    def set_logging_redirect(self, on=False):
        return self.execute(f"set logging redirect {'on' if on else 'off'}")
    
    # def set_logging_debug_redirect(self, on=False):
    #     return self.execute(f"set logging debugredirect {'on' if on else 'off'}")

    def run(self, stdin=None, stdout=None):
        cmd = "run"
        args = ""
        if stdout:
            args += f"> {stdout}"
        if stdin:
            args += f"< {stdin}"
        if len(args) != 0:
            self.execute(f"set args {args}")
        return self.execute(cmd)
    
    def kill(self):
        return self.execute("kill")
    
    def quit(self):
        return self.execute("quit")

gdb_ins = GDBInstance()
