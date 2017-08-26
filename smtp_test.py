# http://dvframes.com/rb/?r=home&m=bbs&bid=programming&iframe=Y&where=subject%7Ctag&keyword=%ED%8C%8C%EC%9D%B4%EC%8D%AC&uid=1440
import smtplib
from email.mime.text import MIMEText

SMTP_MAIL_SERVER_ = 'smtp.gmail.com'
SMTP_ID_ = 'sdjevent@gmail.com'
SMTP_PASSWORD_ = 'sdjvent134679852@'
SMTP_MAIL_SERVER_PORT_ = '587'


def sendMail(FROM_EMAIL_, TO_EMAIL_, subject_, contents_):
    # 한글 메일이 깨진다면 'utf-8'을 'cp949'로 변경 사용
    message_ = MIMEText(contents_, _charset='utf-8')
    message_['Subject'] = subject_
    message_['From'] = FROM_EMAIL_
    message_['To'] = TO_EMAIL_

    sm_ = smtplib.SMTP(SMTP_MAIL_SERVER_, SMTP_MAIL_SERVER_PORT_)
    sm_.ehlo()
    sm_.starttls()
    sm_.login(SMTP_ID_, SMTP_PASSWORD_)
    sm_.sendmail(FROM_EMAIL_, TO_EMAIL_, message_.as_string())
    print('전송완료')
    sm_.quit()