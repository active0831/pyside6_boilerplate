#Standard library modules
import time, uuid
from functools import partial

#Third-party modules
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *

#Custom modules

from lib.helper import MetaSingleton

class Tasks(metaclass=MetaSingleton):
    def __init__(self):
        self.tasks = {}

    def _update_task(self,task_id):
        update_value = self.tasks[task_id].task.update_value
        if update_value != None:
            func = self.tasks[task_id].extern_func_update
            if func != None:
                func(update_value)
        self.tasks[task_id].is_updating = False

    def _finish_task(self,task_id):
        return_value = self.tasks[task_id].task.return_value
        if return_value != None:
            func = self.tasks[task_id].extern_func_return
            if func != None:
                func(return_value)
        del self.tasks[task_id]

    def set(self, task_id, task_object, **kwargs):
        if task_id in self.tasks.keys():
            #old_task = self.tasks[task_id]
            #old_task.terminate()
            #old_task.wait()
            pass
        else:
            newTask = TaskUpdater(task_id, task_object, **kwargs)
            newTask.sig_update.textChanged.connect(self._update_task)
            newTask.finished.connect(partial(self._finish_task,newTask.task_id))
            newTask.start()        
            self.tasks[newTask.task_id] = newTask

    def _repeat_task(self,task_id, task_cls, task_args, **kwargs):
        return_value = self.tasks[task_id].task.return_value

        if return_value != None:
            self.tasks[task_id].extern_func_return(return_value)
        del self.tasks[task_id]
        
        if kwargs["repeat"] > 0:
            kwargs["repeat"] -= 1
        elif kwargs["repeat"] == -1:
            pass
        else:
            return None

        self.repeat(task_id, task_cls, task_args, **kwargs)

    def repeat(self, task_id, task_cls, task_args, **kwargs):
        if task_id in self.tasks.keys():
            #old_task = self.tasks[task_id]
            #old_task.terminate()
            #old_task.wait()
            pass
        else:
            task_object = task_cls(*task_args)
            task_updater = TaskUpdater(task_id, task_object, **kwargs)
            task_updater.sig_update.textChanged.connect(self._update_task)
            task_updater.finished.connect(
                partial(self._repeat_task, task_id, task_cls, task_args, **kwargs))
            task_updater.start()
            self.tasks[task_id] = task_updater

class TaskUpdater(QThread):    
    def __init__(self, task_id, task_object, func_update=None, func_return=None, 
            delay_update=1, delay_return=1, repeat=0, parent=None):
        super().__init__(parent)
        self.task_id = task_id

        self.extern_func_update = func_update
        self.extern_func_return = func_return
        self.delay_update = delay_update
        self.delay_return = delay_return

        self.task = task_object
        self.task.finished.connect(self.finish)

        self.is_updating = False
        self.is_finished = False
        self.sig_update = QLineEdit()
        self.sig_return = QLineEdit()

    def run(self):
        self.task.start()
        while self.is_finished == False:
            time.sleep(self.delay_update)
            if self.is_updating == False:
                self.is_updating = True
                self.update_value = self.task.update_value
                self.sig_update.textChanged.emit(self.task_id)
        time.sleep(self.delay_return)

    def finish(self):
        self.is_finished = True

class AbstractTask(QThread):    
    def __init__(self, *args, parent=None):
        super().__init__(parent)
        self.args = args
        self.update_value = None
        self.return_value = None

    def run(self):
        #print(self.args)
        #for i in range(1000):
        #    time.sleep(0.1)
        #    self.update_value = str(i)
        #self.return_value = "finished"
        #return None
        pass
