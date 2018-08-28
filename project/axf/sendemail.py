import smtplib
from email.mime.text import MIMEText
def sendemail(to,auth_code):
    #邮箱服务器
    mail_server = 'smtp.163.com'
    #用户名
    mail_user = '15194576294@163.com'
    #密码或者授权码
    mail_password = 'lsx199512'
    #生成验证码
    #邮件消息
    message = "【爱先锋登陆验证】"
    #将邮件字符串消息转换邮箱格式
    message = MIMEText(message)
    #设置主题
    message['Subject'] = "【爱先锋】你的验证码为【{}】，请在5分钟内正确输入，打死都不要告诉别人哦！".format(auth_code)
    #设置发送人
    message['From'] = mail_user
    #创建邮件对象
    mail = smtplib.SMTP(mail_server,25)
    mail.login(mail_user,mail_password)
    #发送邮件
    mail.sendmail(mail_user,to,message.as_string())
    mail.quit()
    return 'Ok:200!'






