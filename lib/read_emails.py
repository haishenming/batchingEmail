

import os

from config.conf import BASE_PATH, EMAIL_FILE

def read_emails():
    """ 从文件中读取到邮件列表 """
    emails_list = []
    FILE_PATH = os.path.join(BASE_PATH, 'data', EMAIL_FILE)
    with open(FILE_PATH, 'r') as f:
        for email_pass in f:
            emails_list.append(tuple(email_pass.split("----")))

    return emails_list



if __name__ == '__main__':
    read_emails()