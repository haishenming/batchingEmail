
import re
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr
import poplib

import requests

from config.conf import *




class Email:

    def __init__(self, host, password):
        self.host = host.strip()
        self.password = password.strip()
        self.pop3 = 'pop.163.com'
        self.server = poplib.POP3(self.pop3)

        self.mails = self._connect()

    def _connect(self):
        print(self.server.getwelcome())

        self.server.user(self.host)
        self.server.pass_(self.password)

        messagesCount, messagesSize = self.server.stat()
        print(messagesCount)
        print(messagesSize)

        resp, mails, octets = self.server.list()
        print(resp)
        print(mails)
        print(octets)

        return mails

    def decode_str(self, s):
        value, charset = decode_header(s)[0]
        if charset:
            value = value.decode(charset)
        return value

    def guess_charset(self, msg):
        # 先从msg对象获取编码:
        charset = msg.get_charset()
        if charset is None:
            # 如果获取不到，再从Content-Type字段获取:
            content_type = msg.get('Content-Type', '').lower()
            pos = content_type.find('charset=')
            if pos >= 0:
                charset = content_type[pos + 8:].strip()
        return charset

    def get_email_headers(self, msg):
        """ 获取邮件头 """
        # 邮件的From, To, Subject存在于根对象上:
        headers = {}
        for header in ['From', 'To', 'Subject', 'Date']:
            value = msg.get(header)
            if value:
                if header == 'Date':
                    headers['date'] = value
                if header == 'Subject':
                    # 需要解码Subject字符串:
                    subject = self.decode_str(value)
                    headers['subject'] = subject
                else:
                    # 需要解码Email地址:
                    hdr, addr = parseaddr(value)
                    name = self.decode_str(hdr)
                    value = u'%s <%s>' % (name, addr)
                    if header == 'From':
                        from_address = value
                        headers['from'] = from_address
                    else:
                        to_address = value
                        headers['to'] = to_address
        return headers

    # indent用于缩进显示:
    def get_email_cntent(self, message):
        """ 获取邮件内容 """
        j = 0
        content = ''
        for part in message.walk():
            j = j + 1
            contentType = part.get_content_type()
            if contentType == 'text/plain' or contentType == 'text/html':
                # 保存正文
                data = part.get_payload(decode=True)
                charset = self.guess_charset(part)
                if charset:
                    charset = charset.strip().split(';')[0]
                    data = data.decode(charset)
                content = data
        return content

    def find_the_mail_by_from_host(self, from_host):
        """ 寻找需要的邮件中的url """
        urls = []
        for i, mail in enumerate(self.mails, 1):
            resp, lines, octets = self.server.retr(i)
            try:
                lines = [str(line, 'utf-8') for line in lines]
                msg_content = '\n'.join(lines)
                # 把邮件内容解析为Message对象：
                msg = Parser().parsestr(msg_content)

                msg_headers = self.get_email_headers(msg)
                content = self.get_email_cntent(msg)

                if from_host in msg_headers["from"]:
                    print(msg_headers)
                    print(content)
                    this_urls = re.findall(
                        '.*---\r\n\r\n(.*)\r\n\r\n---.*',
                        content)
                    urls.extend(this_urls)
            except UnicodeDecodeError as e:
                print(e)
                continue
        return urls

def open_urls(urls):
    status_codes = []
    for url in urls:
        response = requests.get(url)
        status_codes.append(response.status_code)

    return status_codes



if __name__ == '__main__':
    pass
    email = Email(HOST, PASSWORD)
    urls = email.find_the_mail_by_from_host(FROM_HOST)
    ret_code = open_urls(urls)



# 输入邮件地址, 口令和POP3服务器地址:
#     emailaddress = 'xxxxxx@163.com'
#     # 注意使用开通POP，SMTP等的授权码
#     password = 'xxxxxx'
#     pop3_server = 'pop.163.com'
#
#     # 连接到POP3服务器:
#     server = poplib.POP3(pop3_server)
#     # 可以打开或关闭调试信息:
#     # server.set_debuglevel(1)
#     # POP3服务器的欢迎文字:
#     print(server.getwelcome())
#     # 身份认证:
#     server.user(emailaddress)
#     server.pass_(password)
#     # stat()返回邮件数量和占用空间:
#     messagesCount, messagesSize = server.stat()
#     print('messagesCount:', messagesCount)
#     print('messagesSize:', messagesSize)
#     # list()返回所有邮件的编号:
#     resp, mails, octets = server.list()
#     print('------ resp ------')
#     print(resp)  # +OK 46 964346 响应的状态 邮件数量 邮件占用的空间大小
#     print('------ mails ------')
#     print(mails)  # 所有邮件的编号及大小的编号list，['1 2211', '2 29908', ...]
#     print('------ octets ------')
#     print(octets)