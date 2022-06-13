
# fin_crawler3

financial crawlers on GCF

## design

https://drive.google.com/file/d/18qINyrg97spgQj_Bzdnn2Ew443PUTm2b/view?usp=sharing
## Setup GCF

1. create project
2. setup GCF
- gcloud functions deploy ... コマンドでAPI承認するか聞いてくるのでYESを選択する
- gcloud functions deploy ... コマンドでデプロイに失敗する場合は数分待ってリトライする

- OAuth同意画面の設定 -> 不要

- APIを検索して有効にする
  - APIとサービスの有効化
    - Cloud Functions API
    - Cloud Build API 
    - Google Drive API
 - Cloud Build APIは
  - 認証情報の設定が必要
    - アプリケーションデータを選択
    - はい、使用しています
    - 次へ
    - 完了
  - Google Drive API
    - 認証情報の作成

3. Test , Exec
  - リソース　→ Cloud Functions API
    - 縦三点リーダー︙から「関数をテスト」
### reference
- <https://blowup-bbs.com/gcp-cloud-functions-python3/>


### 関数のありか

- main.pyに書かないとダメみたい。

## Install Google Cloud SDK

```bash
# Add the Cloud SDK distribution URI as a package source
echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] http://packages.cloud.google.com/apt cloud-sdk main" | sudo tee -a /etc/apt/sources.list.d/google-cloud-sdk.list
# Import the Google Cloud Platform public key
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key --keyring /usr/share/keyrings/cloud.google.gpg add -

# Update the package list and install the Cloud SDK
sudo apt-get update && sudo apt-get install google-cloud-sdk
```

## Deploy

gcloud functions deploy handler --entry-point=handler --runtime python37 --trigger-http --region asia-northeast1 --memory 512MB
gcloud functions deploy handler2 --entry-point=handler --runtime python37 --trigger-http --region asia-northeast1 --memory 512MB


## Google Drive API

- https://zenn.dev/wtkn25/articles/python-googledriveapi-auth
- https://zenn.dev/wtkn25/articles/python-googledriveapi-operation

## How to execute selenium

- ローカルでのスクレイピング作業をGCPに持っていく作戦(その１)
  - <https://qiita.com/kazumatsukazu/items/5b7141c85fd85c7d1c0d>

```bash
git clone https://github.com/ryfeus/gcf-packs.git
cd gcf-packs/selenium_chrome/source
unzip headless-chromium.zip
#gcloud functions deploy handler --runtime python37 --trigger-http --region asia-northeast1 --memory 512MB
gcloud functions deploy gcf_test --entry-point=handler --runtime python37 --trigger-http --region asia-northeast1 --memory 512MB
```

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

