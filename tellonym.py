import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import credentials
import image_editor as editor
from selenium.common.exceptions import ElementNotInteractableException, TimeoutException

DRIVER = webdriver.Chrome(executable_path="C:\\src\\chromedriver\\chromedriver.exe")
URL = "https://tellonym.me/login?redirect=/tells"

class Bot:
    def __init__(self):
        self.loadPage()
        self.agree_options()
        self.number = 0

    def loadPage(self):
        DRIVER.get(URL)
        assert "Tellonym" in DRIVER.title
        email = WebDriverWait(DRIVER, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#root > div > div > div.css-1dbjc4n.r-150rngu.r-eqz5dr.r-16y2uox.r-1wbh5a2.r-11yh6sk.r-1rnoaur.r-1sncvnh > div > div > div.rmq-9213326f > div > div:nth-child(2) > form > div:nth-child(1) > input")))
        email.send_keys(credentials.USERNAME)
        email.send_keys(Keys.TAB)

        password = DRIVER.find_element_by_css_selector("#root > div > div > div.css-1dbjc4n.r-150rngu.r-eqz5dr.r-16y2uox.r-1wbh5a2.r-11yh6sk.r-1rnoaur.r-1sncvnh > div > div > div.rmq-9213326f > div > div:nth-child(2) > form > div:nth-child(2) > input")
        password.send_keys(credentials.PASSWORD)
        password.send_keys(Keys.RETURN)

        send = DRIVER.find_element_by_css_selector("#root > div > div > div.css-1dbjc4n.r-150rngu.r-eqz5dr.r-16y2uox.r-1wbh5a2.r-11yh6sk.r-1rnoaur.r-1sncvnh > div > div > div.rmq-9213326f > div > div:nth-child(2) > form > button > div > div")
        send.click

    def agree_options(self):
        assert "Tellonym" in DRIVER.title
        agree = WebDriverWait(DRIVER, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#qc-cmp2-ui > div.qc-cmp2-footer.qc-cmp2-footer-overlay.qc-cmp2-footer-scrolled > div > button.sc-ifAKCX.hIGsQq")))
        agree.click()
        selected = WebDriverWait(DRIVER, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#qc-cmp2-ui > div.qc-cmp2-footer > div.qc-cmp2-buttons-desktop > button.sc-ifAKCX.hIGsQq")))
        selected.click()

    def get_amount(self):
        tells = DRIVER.find_elements_by_xpath('//*[@id="root"]/div/div/div[5]/div/div/div')
        return len(tells) - 1

    def answer_tells(self, amount):
        for x in range(amount):
            try:
                self.number = self.number + 1
                print(f"Tell No. {self.number}")
                tell = WebDriverWait(DRIVER, 20).until(EC.visibility_of_element_located((By.XPATH, f'//*[@id="root"]/div/div/div[5]/div/div/div[{self.number + 1}]/div/div[1]')))
                tell.click()
                question = WebDriverWait(DRIVER, 20).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="root"]/div/div/div[4]/div/div[2]/div[1]/div/div/span'))).text
                print(f"Question: {question}\nYour Answer:")
                answer = input()
                if "skip" in answer.lower():
                    stop = DRIVER.find_element_by_css_selector("#root > div > div > div:nth-child(2) > div > div:nth-child(2) > div:nth-child(3)")
                    stop.click()
                    raise TimeoutException("Question skipped!")
                image = editor.make_image(question, answer)
                editor.save_image(image, f"tell-{question.replace(' ', '').replace('?', '')[0:15]}")
                textarea = DRIVER.find_element_by_css_selector("#root > div > div > div.css-1dbjc4n.r-150rngu.r-eqz5dr.r-16y2uox.r-1wbh5a2.r-11yh6sk.r-1rnoaur.r-1sncvnh.r-13qz1uu > div > div.rmq-3ca56ea3 > div:nth-child(2) > div > div > div > textarea")
                textarea.send_keys(answer)
                send = DRIVER.find_element_by_css_selector("#root > div > div > div.css-1dbjc4n.r-150rngu.r-eqz5dr.r-16y2uox.r-1wbh5a2.r-11yh6sk.r-1rnoaur.r-1sncvnh.r-13qz1uu > div > div.rmq-3ca56ea3 > div:nth-child(2) > form > button > div > div")
                send.click()
                if DRIVER.title != "Tellonym":
                    feed = WebDriverWait(DRIVER, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#root > div > div > div:nth-child(2) > div > div:nth-child(2) > a:nth-child(3)")))
                    feed.click()
                time.sleep(3)
            except TimeoutException as t:
                print("TimeOutException: {}".format(t.msg))
            except ElementNotInteractableException as v:
                print("ElementNotInteractable: {}".format(v.msg))


if __name__ == "__main__":
    bot = Bot()
    count = bot.get_amount()
    print(f"loaded {count} tells!")
    bot.answer_tells(int(15))
