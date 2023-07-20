from lib.core.state import AbstractState
from lib.core.task import Tasks, AbstractTask
from modules.main import show_status

class State(AbstractState):
    def __init__(self):
        super().__init__()
        self.use("result",[""])

def run():
    Tasks().repeat("run_example", RunTask, ["arg1"], 
        func_update=print, delay_return=1, repeat=-1)

class RunTask(AbstractTask):
    def run(self):
        print("args:",self.args)
        self.update_value = "running..."
        self.return_value = None
        return None