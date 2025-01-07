import json, poplib, email, requests
from modules import settings

class GetMail:
    def __init__(self):
        pass

    def mailToMisskey(self):
        # サーバに接続
        cli = poplib.POP3_SSL(settings.MAIL_POP3_SERVER)
        cli.pop3_port = settings.MAIL_POP3_PORT
        print('(mail)connected.')

        # 認証
        cli.user(settings.MAIL_USER)
        cli.pass_(settings.MAIL_PASSWORD)
        print('(mail)logged in.')

        # メールボックス内のメールの総数を取得
        count = len(cli.list()[1])
        print('(mail)found ' + str(count) + ' messages.')

        headers = {
            'Authorization': f'Bearer {settings.MISSKEY_TOKEN}'
            , 'Content-Type': 'application/json'
        }
        data = {
            'visibility': 'public'
            , 'text': 'text'
        }
        try:
            for i in range(count):
                msg_no = i + 1
                content = cli.retr(msg_no)[1]
                msg = email.message_from_bytes(b'\r\n'.join(content))
                from_ = str(msg['From'])
                print(f'from: {from_}')
                # print(f'msg: {msg}')
                content = self.get_content(msg)
                # print(f'content: {content}')

                # メール内容をtitle,date,contentに分別
                mail_content = self.bunbetu(content)

                # 件名に想定の文章が含まれていない場合はスキップ
                mail_content_subject = mail_content.get('subject')
                print(f'mail_content_subject:{mail_content_subject}')
                if not mail_content_subject:
                    print(f'mail_content_subject is None')
                    continue
                if settings.TARGET_SUBJECT:
                    print('TARGET_SUBJECT: ' + settings.TARGET_SUBJECT)
                    if str(mail_content_subject).find(settings.TARGET_SUBJECT) == -1:
                        continue
                else:
                    print('ALERT!!!: TARGET_SUBJECT is None')

                # Misskeyに投稿
                print(mail_content.get('content'))
                data['text'] = mail_content.get('content') + '\ndate: ' + mail_content.get('date')
                print(settings.HASHTAG)
                if settings.HASHTAG:
                    data['text'] += '\n' + settings.HASHTAG
                res = requests.post(settings.MISSKEY_POST_URL, headers=headers, json=data)
                print(json.loads(res.text))
        finally:
            cli.quit()

    # 本文を取得
    def get_content(self, msg):
        payload = None
        try:
            if msg.is_multipart() is False:
                charset = msg.get_content_charset()
                payload = msg.get_payload(decode=True)
                print(f'charset: {charset}')
                # print(f'payload: {payload}')
                res = payload
                if payload:
                    if charset:
                        res = payload.decode(charset, 'ignore')
                        res = res.replace('\u3000', '  ')
                        print(f'payload(decode by charset): {res}')
                        return res
                    else:
                        res = payload.decode()
                        print(f'payload(decode): {res}')
                        return res
                else:
                    print('payload is ""')
                    return ""
            else:
                res = ''
                for part in msg.walk():
                    charset = part.get_content_charset()
                    payload = part.get_payload(decode=True)
                    print(f'charset: {charset}')
                    # print(f'payload: {payload}')
                    if payload:
                        if charset:
                            tmp = payload.decode(charset, 'ignore')
                            print(f'payload(decode): {tmp}')
                            res += tmp.replace('\u3000', '  ')
                        else:
                            tmp = payload.decode()
                            print(f'payload(decode): {tmp}')
                            res += tmp.replace('\u3000', '  ')
                    else:
                        print('payload is ""')
                print(f'final payload: {res}')
                return res
        except:
            print('payload is not decode')
            return payload

    def bunbetu(self, content:str='')->dict:
        # こういう文章がくるパターンで考えている(違う場合は適宜直してください)
#         text = '''
# ________________________________________
# 差出人: XXXXX<XXXXX@XXXXX.XXXXX.com>
# 送信日時: 2024年12月20日 2:48
# 宛先: XXXXX@outlook.jp <XXXXX@outlook.jp>
# 件名: Misskey通知(仮)

# date: Friday, December 20, 2024 11:43:15 AM
# General お疲れさまです   XXXXXの際にXXXXXを配布する予定です。ついては、配布総数を確認したいので、XXXXXが欲しい方は必要数を投稿してください。   アンケート回答期限：本日15時まで   XXXXX必要数確認アンケート [https://forms.office.com/r/XXXXX]     XXXXX不参加の方でもご希望があれば確保します。   ただし、現在の在庫数XXXXX冊のため、必要数が在庫数を上回る場合には、XXXXX＞XXXXX＞XXXXXの優先順で数量を調整させていただきます。

# Mail From V2
#         '''

        # if content == '':
        #     content = text

        # 上記文章から件名、date、本文を取得
        subject,date = None,None
        content_below_date = ''
        for line in content.split('\n'):
            if line.startswith('Subject:'):
                subject = line.replace('Subject:', '').strip()
            elif line.startswith('date:'):
                date = line.replace('date:', '').strip()
        if date:
            content_below_date = content.split(date, 1)[1].strip()
            content_below_date = content_below_date.split('\nMail From', 1)[0].strip()
            content_below_date = content_below_date.replace('  ', '\n')
        return {
            'subject': subject,
            'date': date,
            'content': content_below_date
        }

if __name__ == '__main__':
    gm = GetMail()
    gm.mailToMisskey()

    #### for test
    # res = gm.bunbetu()
    # print(res)
    # print(res.get('content'))