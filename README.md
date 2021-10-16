
# fin_crawler3

financial crawlers on GCF

## Install Google Cloud SDK

```bash
# Add the Cloud SDK distribution URI as a package source
echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] http://packages.cloud.google.com/apt cloud-sdk main" | sudo tee -a /etc/apt/sources.list.d/google-cloud-sdk.list
# Import the Google Cloud Platform public key
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key --keyring /usr/share/keyrings/cloud.google.gpg add -

# Update the package list and install the Cloud SDK
sudo apt-get update && sudo apt-get install google-cloud-sdk
```

## How to execute selenium

- <https://qiita.com/kazumatsukazu/items/5b7141c85fd85c7d1c0d>

```bash
git clone https://github.com/ryfeus/gcf-packs.git
cd gcf-packs/selenium_chrome/source
unzip headless-chromium.zip
#gcloud functions deploy handler --runtime python37 --trigger-http --region asia-northeast1 --memory 512MB
gcloud functions deploy gcf_test --entry-point=handler --runtime python37 --trigger-http --region asia-northeast1 --memory 512MB
```

- ローカルでのスクレイピング作業をGCPに持っていく作戦(その１)
  - https://qiita.com/kazumatsukazu/items/5b7141c85fd85c7d1c0d

## Prepare

1. install chromedriver
2. install selenium

```bash
pip install selenium
```

# Rakuten Crawler
## usage
```
python rakuten_crawler.py YOUR-USER-ID YOUR-PASSWORD [--outdir <dir>]
```

# VIEW Card Crawler
## usage
```
python view_crawler.py YOUR-USER-ID YOUR-PASSWORD [--outdir <dir>]
```

# AEON Card Crawler
## usage
```
python aeon_crawler.py YOUR-USER-ID YOUR-PASSWORD [--outdir <dir>]
```

# Password Encrypt Hint(for Linux)
## prepare(generate key pair)
``
ssh-keygen -t rsa -b 4096 -m PEM
```
```
ssh-keygen -t rsa
ssh-keygen -e -m PEM -f ~/.ssh/id_rsa > ~/.ssh/id_rsa.pem
ssh-keygen -e -m PKCS8 -f ~/.ssh/id_rsa.pub  > ~/.ssh/id_rsa.pub.pem
```

## generate encrypted password file
```
echo "yourpassword" | openssl rsautl -encrypt -pubin -inkey ~/.ssh/id_rsa.pub.pem -out secretfile
```

## use password file
```
echo `openssl rsautl -decrypt -inkey ~/.ssh/id_rsa -in secretfile`
```

## see also
https://qiita.com/kugyu10/items/b27d99f6df67a3b6c348
https://www.masatom.in/pukiwiki/Linux/%25B8%25F8%25B3%25AB%25B8%25B0%25B0%25C5%25B9%25E6/


## TODO
### SBI Crawler
済- 口座管理->保有証券>CSV
済- トータルリターン→CSV
- 取引履歴→照会->CSV
- 譲渡益税明細→照会→CSV
- 外貨建口座→照会→CSV
- 入出金・振替→入出金明細→CSV
- 外貨入出金→CSV

