"""
pycralwer.py
"""
import os
import sys
import logging
import logging.handlers
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent

class PyCrawlea:
    """This is a Common Crawler class."""
    driver = None
    ss_seq = 1
    screenshot_dir = "."
    is_save_html_with_ss = False

    def __init__(self, out_dir, user_agent=""):
        options = Options()
        options.add_argument('--headless')
#        options = webdriver.ChromeOptions()
        options.add_experimental_option("prefs", {"download.default_directory": out_dir })
        if user_agent != '':
            options.add_argument('--user-agent='+user_agent)
        else:
            ua = UserAgent()
            options.add_argument('--user-agent='+ua.safari)

        driver = webdriver.Chrome(options=options)
        driver.set_page_load_timeout(10)
        # windowサイズを変更
        win_size = driver.get_window_size()
        driver.set_window_size(win_size['width']+200,win_size['height']+400)
        self.driver = driver

    def screenshot(self, seq=None, name='ss'):
        '''
        スクリーンショットを撮る
        '''
        seq = self.ss_seq if seq is None else seq
        fname = os.path.join(self.screenshot_dir,'{}_{}.png'.format(seq, name))
        self.driver.get_screenshot_as_file(fname)
        if self.is_save_html_with_ss:
            self.save_page(seq,name)
        self.ss_seq += 1
        return fname

    def get_downloaded_filename(self, dir):
        """
        ダウンロードされたファイル名を取得する
        """
        if len(os.listdir(dir)) == 0:
            return None
        return max (
            [os.path.join(dir, f) for f in os.listdir(dir)], key=os.path.getctime
        )

    def save_page(self, seq=None, name='ss'):
        '''
        HTMLソースを保存
        '''
        seq = self.ss_seq if seq is None else seq
        fname = os.path.join(self.screenshot_dir,'{}_{}.html'.format(seq,name))
        with open(fname, 'wt') as out:
            out.write(self.driver.page_source)
        return fname



if __name__ == '__main__':
    main = PyCrawler(".")
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")
    log = logging.getLogger(main.__class__.__name__)
    log.info("start")
    main.is_save_html_with_ss = True
    main.driver.get("https://www.ugtop.com/spill.shtml")
    main.screenshot(name="kakunin")
    log.info("end")
