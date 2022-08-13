# coding: utf-8
"""
pycralwer.py
"""
import os
import logging
import logging.handlers
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent


class PyCrawler:
    """This is a Common Crawler class."""
    DEFAULT_OUT_DIR = "."
    screenshot_dir = "."
    out_dir = DEFAULT_OUT_DIR
    log_dir = "./log"
    driver = None
    ss_seq = 1
    is_save_html_with_ss = False
    DEFAULT_PAGE_LOAD_TIMEOUT = 10

    def __init__(self, out_dir=None, user_agent=None):
        self.out_dir = out_dir if out_dir is None else self.out_dir
        options = Options()
        options.add_argument('--headless')
#        options = webdriver.ChromeOptions()
        options.add_experimental_option("prefs", {"download.default_directory": out_dir})
        agent = user_agent if user_agent is not None else UserAgent().safari
        options.add_argument(f'--user-agent={agent}')

        driver = webdriver.Chrome(options=options)
        driver.set_page_load_timeout(self.DEFAULT_PAGE_LOAD_TIMEOUT)
        # windowサイズを変更
        win_size = driver.get_window_size()
        driver.set_window_size(win_size['width'] + 200, win_size['height'] + 400)
        self.driver = driver

    def __del__(self):
        if self.driver is not None:
            self.driver.quit()

    def screenshot(self, seq=None, name='ss'):
        '''
        スクリーンショットを撮る
        '''
        seq = self.ss_seq if seq is None else seq
        fname = os.path.join(self.screenshot_dir, '{}_{}.png'.format(seq, name))
        self.driver.get_screenshot_as_file(fname)
        if self.is_save_html_with_ss:
            self.save_page(seq, name)
        self.ss_seq += 1
        return fname

    def get_downloaded_filename(self, download_dir):
        """
        ダウンロードされたファイル名を取得する
        """
        if len(os.listdir(download_dir)) == 0:
            return None
        return max(
            [os.path.join(download_dir, f) for f in os.listdir(download_dir)], key=os.path.getctime
        )

    def save_page(self, seq=None, name='ss'):
        '''
        HTMLソースを保存
        '''
        seq = self.ss_seq if seq is None else seq
        fname = os.path.join(self.screenshot_dir, '{}_{}.html'.format(seq, name))
        with open(fname, 'wt') as out:
            out.write(self.driver.page_source)
        return fname


if __name__ == '__main__':
    main = PyCrawler(".")
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")
    log = logging.getLogger(main.__class__.__name__)
    log.info("start")
    URL = "https://www.ugtop.com/spill.shtml"
    log.info("getting %s", URL)
    main.is_save_html_with_ss = True
    main.driver.get(URL)
    main.screenshot(name="kakunin")
    log.info("snapshot is saved to %s", main.screenshot_dir)
    log.info("end")
