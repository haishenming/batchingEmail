import smtplib

from_addr = "taowuyoujz92404@163.com"
password = "jiegu6980"
smtp_server = "smtp.163.com"  # <span style="color: #ff0000;">your email send server</span>
to_addr = "haishenmingx@gmail.com"

server = smtplib.SMTP()
server.connect(smtp_server)
server.login(from_addr, password)
server.sendmail(from_addr, to_addr, "123")
server.quit()

print("your result has sent to your email!")