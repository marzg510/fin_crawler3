# coding: utf-8

from rakuten_crawler import RakutenCrawler

def rakuten_crawler(request):
    line = "Hello,rakuten_crawler!"
    print(line)
    print
    RakutenCrawler().crawl(request)
    return line


if __name__ == "__main__":
    rakuten_crawler(None)
