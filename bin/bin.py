
from config.conf import *

from lib.op_email import Email, open_urls
from lib.read_emails import read_emails



if __name__ == '__main__':
    emails = read_emails()
    for i, email_host_email_password in enumerate(emails, 1):
        print("-------------- 第 {} 个, 共 {} 个 -------------"
              .format(i, len(emails)))
        email_host, email_password = email_host_email_password
        email = Email(email_host, email_password)

        urls = email.find_the_mail_by_from_host(FROM_HOST)
        ret_code = open_urls(urls)

        for code in ret_code:
            if code != 200:
                print("有错")
            else:
                print("请求成功！")

    print("完成")