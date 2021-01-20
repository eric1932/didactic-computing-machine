from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException

from jobs.example import JobTemplate

URL = "https://www.summer-plus.net/"
PAGE_TASK = "https://www.summer-plus.net/plugin.php?H_name-tasks.html"
PAGE_REWARD = "https://www.summer-plus.net/plugin.php?H_name-tasks-actions-newtasks.html.html"


class Job(JobTemplate):
    def __init__(self):
        super().__init__("south-plus")

    def exec(self):
        driver = self.get_driver_chrome(False, use_profile=True)
        try:
            driver.set_page_load_timeout(5)
            try:
                driver.get(URL)
            except TimeoutException:
                pass
            logged_in = False
            try:
                driver.find_element_by_id("logintab")
            except NoSuchElementException:
                logged_in = True
            if not logged_in:
                # cannot continue, need manual operation
                to_return = ("fail", "needs login")
            else:
                driver.get(PAGE_TASK)
                tasks = driver.find_elements_by_css_selector("a[title=按这申请此任务]")
                for t in tasks:
                    t.click()
                driver.get(PAGE_REWARD)
                rewards = driver.find_elements_by_css_selector("a[title=领取此奖励]")
                for r in rewards:
                    r.click()
                print("Count:", len(tasks))
                to_return = ("success", f"count={len(tasks)}")
        finally:
            driver.close()
            return to_return
