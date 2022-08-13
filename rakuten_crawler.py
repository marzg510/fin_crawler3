# coding: utf-8
"""
Rakuten Card Crawler
"""

import logging
import logging.handlers
import sys
import os
from argparse import ArgumentParser
import time
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
    引数解析器の取得
    """
    usage = 'Usage: python %s USER_ID PASSWORD [--outdir <dir>] [--help]'\
            % os.path.basename(__file__)
    parser = ArgumentParser(usage=usage)
    parser.add_argument('user_id', type=str, help='USER ID 1')
    parser.add_argument('passwd', type=str, help='PASSWORD')
    parser.add_argument('-o', '--outdir', type=str, help='file output directory',
                        default=PyCrawler.DEFAULT_OUT_DIR)
    return parser


class RakutenCrawler(PyCrawler):
    """
    This is a Rakuten Crawler class.
    """
    log = logging.getLogger()
    out_dir = "."
    outfile = None

    def __init__(self, user_id, passwd, out_dir=None, log=None):
        self.user_id = user_id
        self.passwd = passwd
        if log is not None:
            self.log = log
        if out_dir is not None:
            self.out_dir = out_dir
        super().__init__(out_dir)

    def write_future_expence(self, driver):
        """
        未確定支払い分の書き込み
        """
        log = self.log
        log.info("write furure expence to %s", self.out_dir)
        e_month = driver.find_element(By.XPATH, '//div[@id="js-payment-calendar"]')
        log.debug('month : tag=%s, text=%s',e_month.tag_name, e_month.text)
        e_bill = driver.find_element(By.XPATH, '//div[@class="stmt-about-payment__money__main"]')
        e_mark = e_bill.find_element(By.XPATH, 'mark')
        log.debug('mark : tag=%s text=%s',e_mark.tag_name, e_mark.text)
        e_amount = e_bill.find_element(By.XPATH,
                                       'div[@class="stmt-about-payment__money__main__num"]')
        log.debug('amount : tag=%s text=%s',e_amount.tag_name, e_amount.text)
        with open(
            os.path.join(self.out_dir, '%s_%s.txt' % (e_month.text, e_mark.text)), 'wt'
        ) as fout:
            fout.write(e_amount.text)

    def crawl(self):
        """
        クローリングメイン
        """
        log = self.log
        driver = self.driver
        log.info("user_id=%s", self.user_id)
        log.info("outdir=%s", self.out_dir)
        log.info("screenshot_dir=%s", self.screenshot_dir)
        # ############# 楽天ログイン画面
        log.info("getting Rakuten login page")
        driver.get('https://www.rakuten-card.co.jp/e-navi/')
        time.sleep(1)
        self.screenshot(name='login')
        # ############# ログイン
        log.info("logging in to the site...")
        log.info("logging in to the site...")
        e_user = driver.find_element(By.ID, 'u')
        e_password = driver.find_element(By.ID, 'p')
        e_user.send_keys(self.user_id)
        e_password.send_keys(self.passwd)
        e_button = driver.find_element(By.ID, 'loginButton')
        self.screenshot(name='before-login')
        e_button.click()
        time.sleep(3)
        self.screenshot(name='top')
        # ############ ご利用明細へのリンクを探しクリック
        log.info("navigate to bill-detail..")
        e_link = driver.find_element(By.XPATH, '//ul[@class="rce-u-list-plain"]//a[text()="ご利用明細"]')
        log.debug('link for detail : tag=%s href=%s visible=%s',
                  e_link.tag_name, e_link.get_attribute('href'), e_link.is_displayed())
        # ご利用明細
        e_link.click()
        time.sleep(1)
        self.screenshot(name='detail')
        # ############ 確定かどうか判定
        e_bill = driver.find_element(By.XPATH, '//div[@class="stmt-about-payment__money__main"]')
        log.debug('bill-text:%s', repr(e_bill.text))
        # ############ 未確定なら支払い予定額を保存
        if '未確定' in e_bill.text:
            self.write_future_expence(driver)
            log.info("支払いが未確定なので、予定金額だけ出力して処理を終了します")
            return
        # ############ CSVダウンロードのリンクを探しクリック
        log.info("downloading csv..")
        e_csv_link = driver.find_element(By.XPATH, '//a[contains(.,"CSV")]')
        log.debug('link for csv : tag=%s href=%s visible=%s',
                  e_csv_link.tag_name, e_csv_link.get_attribute('href'), e_csv_link.is_displayed())
        # download csv
        driver.get(e_csv_link.get_attribute('href'))
        time.sleep(1)
        self.screenshot(name='csv_downloaded')
        # ############ 次月が押せたら次月を押す
        log.info("navigate to next month ..")
        e_next_link = driver.find_element(By.XPATH, '//a[text()="次月"]')
        log.debug('link for next month : tag=%s href=%s visible=%s',
                  e_next_link.tag_name, e_next_link.get_attribute('href'),
                  e_next_link.is_displayed())
        e_next_link.click()
        time.sleep(1)
        self.screenshot(name='next_month')
        # ############ 支払い予定金額出力
        self.write_future_expence(driver)


def main():
    """ main """
    ap_name = os.path.splitext(os.path.basename(__file__))[0]
    log = get_logger(ap_name)
    log.info("start")
    parser = get_arg_parser()
    args = parser.parse_args()
    user_id = args.user_id
    passwd = args.passwd
    outdir = args.outdir
    crawler = RakutenCrawler(user_id, passwd, outdir, log)
    crawler.is_save_html_with_ss = True
    crawler.screenshot_dir = "./log/ss_rakuten"
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
