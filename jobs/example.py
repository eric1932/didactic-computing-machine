import abc
import os.path
import threading
from datetime import datetime
from datetime import timedelta

from selenium import webdriver


class JobTemplate:
    def __init__(self, module_name):
        # TODO read from file
        self.module_name = module_name
        if os.path.exists(f"./logs/{module_name}.time.txt"):
            with open(f"./logs/{module_name}.time.txt") as f:
                line = f.readline()
                if "." in line:
                    self.last_success_time = datetime.strptime(line, '%Y-%m-%d %H:%M:%S.%f')
                else:
                    self.last_success_time = datetime.strptime(line, '%Y-%m-%d %H:%M:%S')
            self.return_status = {"status": "success", "time": self.last_success_time}
        else:
            self._set_last_success_time(datetime.min)
            self.return_status = {"status": "first-run"}
        self.thread_lock = False
        self.worker_thread = threading.Thread(target=self.watcher)

    @abc.abstractmethod
    def exec(self):
        """
        Abstract method. Execute arbitrary code.
        """
        pass

    def call(self):
        """
        Check if last run was before a day.
        If so, start a new thread of watcher() and return in-progress.
        Else, return success.
        :return: status json shown in the web page
        """
        if datetime.utcnow() > self.last_success_time + timedelta(days=1):
            prev_status = self.return_status
            self.return_status = {"status": "in-progress"}
            if self.return_status["status"] == "first-run":
                return_status = self.return_status
            else:
                return_status = prev_status
            if not self.thread_lock:  # wait for finish
                self.thread_lock = True
                self.worker_thread.start()  # start a self.watcher
            return return_status
        else:
            return self.return_status

    def watcher(self):
        """
        Call self.exec() and see if any exception occurs,
        and set the status & log time accordingly
        """
        try:
            ret, _ = self.exec()
            if ret == "success":
                self.worker_thread = threading.Thread(target=self.watcher)
                self.thread_lock = False
            self._set_last_success_time(datetime.now())
            # set success
            self.return_status = {"status": "success", "time": self.last_success_time}
        except Exception:  # TODO
            # set failure
            self.return_status = {"status": "failure"}

    @staticmethod
    def get_driver_chrome(headless=True):
        options = webdriver.ChromeOptions()
        options.headless = headless
        return webdriver.Chrome(options=options)

    def _set_last_success_time(self, time: datetime):
        self.last_success_time = time
        with open(f"./logs/{self.module_name}.time.txt", "w") as f:
            f.write(f"{time}")
