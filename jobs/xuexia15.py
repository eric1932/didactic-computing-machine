import json

from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from jobs.example import JobTemplate

# Constants
URL = "https://www.xuexia15.cc/forum.php"


class Job(JobTemplate):
    def __init__(self):
        super().__init__("xuexia15")

    def exec(self):
        with open("./credentials/xuexia15.json") as f:
            cred_dict = json.loads(f.read())
        USER = cred_dict["username"]
        PASS = cred_dict["password"]

        driver = JobTemplate.get_driver_chrome()

        try:
            # Part 1: handle log in
            # don't want to wait for too long
            driver.set_page_load_timeout(5)  # driver.get timeout
            # driver.set_script_timeout(5)
            try:
                driver.get(URL)
            except TimeoutException:
                pass  # just continue
            '''
            # import cookies *if exist*
            if os.path.exists("./credentials/xuexia15_cookies.json"):
                with open("./credentials/xuexia15_cookies.json") as f:
                    c = json.loads(f.read())
                    if isinstance(c, list):
                        for each_c in c:
                            driver.add_cookie(each_c)
                    else:
                        driver.add_cookie(c)
                try:
                    driver.refresh()
                except Exception:
                    pass
            '''
            # check login status
            logged_in = True
            try:
                driver.find_element_by_id("um")
            except NoSuchElementException:
                logged_in = False
            if not logged_in:
                user = driver.find_element_by_id("ls_username")
                user.send_keys(USER)
                pwd = driver.find_element_by_id("ls_password")
                pwd.send_keys(PASS)
                btn_login = driver.find_element_by_css_selector(
                    "form#lsform>div:first-child>div>table>tbody>tr:nth-child(2)>td:nth-child(3)>button")
                btn_login.click()
                # TODO simplify
                driver.set_page_load_timeout(10)
                try:
                    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#um")))
                except Exception:
                    pass

            assert driver.find_element_by_id("um")

            # Part 2: click 打卡签到
            qiandao = driver.find_elements_by_xpath("//*[contains(text(), '打卡签到')]")[0]
            qiandao.click()

            # TODO add validation

            # Save cookies (failed to load because of unknown issue)
            '''
            cookies = driver.get_cookies()
            with open("./credentials/xuexia15_cookies.json", "w") as f:
                f.write(json.dumps(cookies))
            '''
        finally:
            driver.quit()
