import time
import logging
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By

class Disney:
    def __init__(self):
        self.url = "https://reserve.tokyodisneyresort.jp/en/ticket/search/"
        self.candidate_days = list(range(1, 20))
        self.sleep_sec = 5

    def send_notification(self, day):
        data = {
            "chat_id": "<chat_id>",
            "text": f"Tickets available on Nov. {day}",
        }
        requests.post(
            "https://api.telegram.org/bot<token>/sendMessage",
            data=data,
        )

    def snap_up(self):
        self.driver = webdriver.Chrome("./chromedriver")
        # self.driver.maximize_window()
        self.driver.get(self.url)
        logging.info(self.driver.title)
        self.driver.find_element(
            By.XPATH, "//a[contains(@class,'button-circle')]"
        ).click()
        time.sleep(self.sleep_sec)
        self.driver.find_element(By.XPATH, '//button[text()="Next"]').click()

        while(True):
			for day in self.candidate_days:
				time.sleep(self.sleep_sec + 5)
				logging.info(f"Looking for day: {day}")
				self.driver.find_element(
				By.XPATH,
				f"//tbody[contains(@data-month,'11')]/tr/td/a[contains(@data-day,'{day}')]",
				).click()
				time.sleep(self.sleep_sec)
				self.driver.find_element(
				By.XPATH, '//button[text()="Print out at home"]'
				).click()
				time.sleep(self.sleep_sec)

				unvailable_cnt = len(
				self.driver.find_elements(
					By.XPATH,
					'//p[text()="Currently not available for purchase"]',
				)
				)
				# 3 types of tickets in total
				if unvailable_cnt < 3:
				logging.info("Tickets Available!!!")
				self.send_notification(day)
				break
			time.sleep(300)


if __name__ == "__main__":
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    disney = Disney()
    disney.snap_up()
