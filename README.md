# mail-to-misskey

## 概要

* (PowerAutomateなどで送られてきた)メールをもとにMisskeyに投稿するPythonです

## 使い方

* `git clone https://github.com/tetsuya-ki/mail-to-misskey.git`
  * リポジトリをクローンする
* メールのPOP3サーバーのURL、ポート、ユーザー、パスワードを取得する
  * GMailの場合はパスワードはアプリパスワードが必要(2段階認証をしないとダメかも)
* Misskeyの投稿用URLを取得
  * <https://xxxx.com/api-doc>を開き、notes/createを検索
  * <https://xxxx.com/api/notes/create>のようなもののはず
  * Misskey Hubの説明: <https://misskey-hub.net/ja/docs/for-developers/api/endpoints/>
* Misskeyの投稿用トークンを取得(Misskey v2024.11.0の場合)
  * 設定＞API＞アクセストークンの発行を選択
  * 名前を適当につけ、「ノートを作成・削除する」だけ有効にし、右上のチェックする
  * 生成されたトークンを利用する
* modules/filesにある「.env.sample」をもとに「.env」を作成する
  * 以下の「環境変数」のところをみつつ設定する
* ためしに動かしてみる
  * `poetry install`
    * 利用しているモジュールをインストールする
  * `poetry run python getmail.py`
    * pythonを実行する

### 環境変数

* MISSKEY_POST_URL
  * `https://xxxx/api/notes/create`みたいなやつ
* MISSKEY_TOKEN
  * `xxxxx`みたいなトークン
* MAIL_POP3_SERVER
  * メールサーバーのPOP3アドレス。`pop.xxxx.com`みたいなやつ
* MAIL_POP3_PORT
  * メールサーバーのPOP3ポート。`995`みたいなやつ(SSL)
* MAIL_USER
  * メールサーバーにログインするためのユーザー。`yyyy@xxxx.com`みたいなやつ
* MAIL_PASSWORD
  * メールサーバーにログインするためのパスワード。`zzzzzzzzzzzzzzz`みたいなやつ
* HASHTAG
  * Misskeyに投稿する時のハッシュタグ。`"#お知らせ #ねこ大好き"`みたいに複数も可能。自分で「#」をつけてください。これは`"`で囲う必要があります！
* TARGET_SUBJECT
  * Misskey投稿する対象のメールの件名

## systemd-timerを利用して定期的に実行する

* systemd-timerを設定(以下記事などを参考にする)
  * <https://qiita.com/sugichan55/items/219cb24b77d66f112b10>
* serviceファイルをまず作る
  * /etc/systemd/system/mail2misskey.service
  * WorkingDirectoryは自分の使っているところに変更すること！
    * 自分は `sudo vim /etc/systemd/system/mail2misskey.service`でつくる派閥(なんでもいいと思う)

```ini
[Unit]
Description=mail to misskey

[Service]
Type=oneshot
User=ubuntu
WorkingDirectory=/home/ubuntu/python/mail-to-misskey
ExecStart=/usr/bin/poetry run python getmail.py

[Install]
WantedBy=multi-user.target
```

* timerファイルを作成
  * /etc/systemd/system/mail2misskey.timer
  * OnCalendarはいい感じに設定する！
    * `systemd-analyze calendar "*-*-* *:00:00"`みたいにすると確認できる
    * これは1時間ごとに実行する設定

```ini
[Unit]
Description=Timer for mail to misskey

[Timer]
OnCalendar=*-*-* *:00:00
# これは1時間ごと
#OnCalendar=*:00/5
# これは5分ごと(コメントアウト)
Persistent=true

[Install]
WantedBy=timers.target
```

* タイマー設定の有効化
  * `sudo systemctl enable mail2misskey.timer`
* タイマー設定の起動
  * `sudo systemctl start mail2misskey.timer`
* タイマー設定の確認
  * `systemctl status mail2misskey.timer`
* vimで編集したらリロードする
  * `sudo systemctl daemon-reload`
