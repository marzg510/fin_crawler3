# coding: utf-8
"""
SMBC Crawler
"""

import logging
import logging.handlers
import sys
import os
from argparse import ArgumentParser
import time
import selenium.common.exceptions
from selenium.webdriver.common.by import By
from pycrawler import PyCrawler


def get_logger(name):
    """
    ログ設定
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
#    handler = logging.StreamHandler(sys.stdout)
    handler = logging.handlers.TimedRotatingFileHandler('%s/%s.log' % ("./log", name), 'D', 2, 13)
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s"))
    logger.addHandler(handler)
    return logger


def get_arg_parser():
    """
    引数解析機の取得
    """
    usage = 'Usage: python %s '\
            'USER_ID1 USER_ID2 PASSWORD ACCOUNT_NO [--outdir <dir>] [--url <url>] [--help]'\
            % os.path.basename(__file__)
    parser = ArgumentParser(usage=usage)
    parser.add_argument('user1', type=str, help='USER ID 1')
    parser.add_argument('user2', type=str, help='USER ID 2')
    parser.add_argument('passwd', type=str, help='PASSWORD')
    parser.add_argument('account', type=str, help='ACCOUNT_NO')
    parser.add_argument('-o', '--outdir', type=str, help='file output directory', default="out/")
    return parser


class SmbcCrawler(PyCrawler):
    """
    This is a SMBC Crawler class.
    """
#    ap_name = os.path.splitext(os.path.basename(__file__))[0]
    log = logging.getLogger()
    out_dir = "."
    outfile = None

    def __init__(self, user1, user2, passwd, account, out_dir=None, log=None):
        self.user1 = user1
        self.user2 = user2
        self.passwd = passwd
        self.account = account
        if log is not None:
            self.log = log
        if out_dir is not None:
            self.out_dir = out_dir
        super().__init__(out_dir)
        self.outfile = os.path.join(
            self.out_dir,
            'smbc_%s_%s.csv' % (account, time.strftime('%Y%m%d', time.localtime()))
        )

    def crawl(self):
        """
        クローリングメイン
        """
        log = self.log
        driver = self.driver
        log.info("user_id=%s %s", self.user1, self.user2)
        log.info("account=%s", self.account)
        log.info("outdir=%s", self.out_dir)
        log.info("outfile=%s", self.outfile)
        log.info("screenshot_dir=%s", self.screenshot_dir)
        # ############# ログイン画面
        log.info("getting SMBC login page")
        driver.get('https://direct.smbc.co.jp/aib/aibgsjsw5001.jsp')
        time.sleep(1)
        self.screenshot(name='smbc_login')
        # ############# system maintainance check
        try:
            e_sorry = driver.find_element(By.CSS_SELECTOR, 'div#sorry')
            log.error("システムメンテナンス中:%s", e_sorry)
            log.error("error end")
            sys.exit(9)
        except selenium.common.exceptions.NoSuchElementException:
            pass
        # ############# ログイン
        log.info("logging in to the site...")
        e_tab = driver.find_element(By.ID, 'tab-switchB02')
        e_tab.click()
        time.sleep(1)
        self.screenshot(name='smbc_login_tab_clicked')
        e_user1 = driver.find_element(By.NAME, 'userId1')
        e_user2 = driver.find_element(By.NAME, 'userId2')
        e_password = driver.find_element(By.ID, 'inputpassword')
        e_user1.send_keys(self.user1)
        e_user2.send_keys(self.user2)
        e_password.send_keys(self.passwd)
        self.screenshot(name='before-login')
        e_submit = driver.find_element(By.XPATH, "//div[@class='btn-wrap']/a[.='ログイン']")
        e_submit.click()
        time.sleep(3)
        self.screenshot(name='after-login')
        # ############ login check
        log.info("checking login...")
        e_errs = driver.find_elements(
            By.XPATH, "//dt[@class='title' and contains(text(),'エラーコード')]"
        )
        if len(e_errs) > 0:
            log.error("login failure")
            for err in e_errs:
                log.error(err)
            raise Exception('login failure')
        # ############ confirm message
        log.info("confirming message...")
        e_next = driver.find_elements(By.XPATH, '//span[text()="確認して次へ"]/..')
        if e_next:
            e_next[0].click()
        else:
            log.info("no messages to confirm")
        self.screenshot(name='smbc-top-after-confirm')
        # ############ Navigate to Detail page
        log.info("Navigate to Detail page...")
        e_link = driver.find_element(By.XPATH, "//a[contains(@onclick,'{}')]".format(self.account))
        log.debug('link for detail : tag=%s href=%s visible=%s',
                  e_link.tag_name, e_link.get_attribute('href'), e_link.is_displayed())
        e_link.click()
        time.sleep(1)
        self.screenshot(name='detail')
        # ############ 過去の明細を照会
        e_button = driver.find_element(By.XPATH, "//button[span[contains(text(),'過去の明細を照会')]]")
        log.debug('button for past datail : tag=%s visible=%s',
                  e_button.tag_name, e_button.is_displayed())
        e_button.click()
        time.sleep(3)
        self.screenshot(name='past_detail_dialog')
        # ############ 照会
        e_button = driver.find_element(By.XPATH, "//button[@data-mode='照会']")
        log.debug('button for show : tag=%s visible=%s', e_button.tag_name, e_button.is_displayed())
        e_button.click()
        time.sleep(3)
        self.screenshot(name='past_detail')
        # ############ 並べ替え
        e_button = driver.find_element(By.XPATH, "//button[@aria-label='並替']")
        log.debug('button for sort : tag=%s visible=%s', e_button.tag_name, e_button.is_displayed())
        e_button.click()
        self.screenshot(name='sort')
        # ############ 明細が古い順
        e_button = driver.find_element(
            By.XPATH,
            "//li[label[input[@type='radio' and @name='accountSort' and @value='desc']]]"
        )
        log.debug('button for sort desc : tag=%s visible=%s',
                  e_button.tag_name, e_button.is_displayed())
        e_button.click()
        self.screenshot(name='sorted_descention')
        # ############ Download CSV file
        log.info("Downloading")
        e_csv = driver.find_element(By.XPATH, "//a[contains(.,'明細をCSVダウンロード')]")
        log.debug('link for csv : tag=%s href=%s visible=%s',
                  e_csv.tag_name, e_csv.get_attribute('href'), e_csv.is_displayed())
        e_csv.click()
        log.info("finish file writing to %s", self.out_dir)
        self.screenshot(name='after-csv-downloaded')
        # rename
        time.sleep(10)
        os.rename(os.path.join(self.out_dir, 'meisai.csv'), self.outfile)
        log.info("rename file to {}".format(self.outfile))


def main():
    """ main """
    ap_name = os.path.splitext(os.path.basename(__file__))[0]
    log = get_logger(ap_name)
    log.info("start")
    parser = get_arg_parser()
    args = parser.parse_args()
    user1 = args.user1
    user2 = args.user2
    passwd = args.passwd
    account = args.account
    outdir = args.outdir
    crawler = SmbcCrawler(user1, user2, passwd, account, outdir, log)
    crawler.is_save_html_with_ss = True
    crawler.screenshot_dir = "./log/ss_smbc"
    crawler.driver.set_page_load_timeout(60)
    try:
        crawler.crawl()
    except Exception as ex:
        log.exception('exception occurred.')
        print(ex, file=sys.stderr)
    finally:
        del crawler

    log.info("end")


if __name__ == '__main__':
    main()
    exit()
