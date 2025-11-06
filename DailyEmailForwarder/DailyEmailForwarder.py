import zmail

from datetime import datetime, timedelta
import pytz

# 一、读取邮件并打包成汇总邮件
# 1. ❗配置被读取的邮箱
server = zmail.server("被读取的邮箱", "相应授权码") #改为邮箱地址和授权码

# 2. 获取最近24小时内的邮件（时间范围可换）
# 获取所有邮件
mails = server.get_mails() # 所以最好养成清收件箱的习惯

# 过滤出24小时内的邮件
tz_shanghai = pytz.timezone("Asia/Shanghai") # 增加时区，以东八为例
time_cutoff = datetime.now(tz_shanghai) - timedelta(hours=24)

recent_mails = []

for mail in mails:
    mail_date = mail.get("Date", "")
    try:
        if mail_date >= time_cutoff:
            recent_mails.append(mail)
    except:
        recent_mails.append(mail) # 解析失败也保留

# 3. 打包成一封汇总邮件
# 邮件标题
summary_subject = f"××邮箱 | 过去24小时新增 {len(recent_mails)} 封邮件" # 标题自己起

# 邮件抬头（如果换时间记得改一下）
summary_content = f"""
最新获取时间：{datetime.now(tz_shanghai)}
过去24小时共收到 {len(recent_mails)} 封邮件
{"="*40}
"""

# 把邮件内容打包进汇总邮件
if recent_mails:
    for n, recent_mail in enumerate(recent_mails, 1):

        subject = recent_mail.get("Subject") or "无主题"
        from_ = recent_mail.get("From") or "未知发件人"
        date = recent_mail.get("Date") or "时间未知"
        original_content = "".join(recent_mail.get("content_text")) or "此邮件无纯文本正文，可能为HTML或附件。"
        original_attachment = "此邮件包含附件。" if recent_mail.get("attachment") else "此邮件无附件。"

        summary_content += f"""
{n}
原邮件主题：{subject}
原邮件发件人：{from_}
原邮件日期：{date}
------------------------------ 原邮件内容 ------------------------------
{original_content}
------------------------------
{original_attachment}
"""

# 终端可见
print(summary_content)



import smtplib
from email.mime.text import MIMEText

# 二、转发汇总邮件
# 1. ❗配置邮箱（换工具了，被读取的邮箱需再次配置！）
work_email = "被读取的邮箱"
work_password = "相应授权码" # 授权码
work_smtp_server = "smtp.相应服务器地址" # smtp服务器地址
personal_email = "收汇总邮件的邮箱" # 收邮件的邮箱只需地址

# 2. 发送汇总邮件
try:
    # 创建邮件
    msg = MIMEText(summary_content, "plain", "utf-8")
    msg["Subject"] = summary_subject
    msg["From"] = work_email
    msg["To"] = personal_email
    
    # 发送
    with smtplib.SMTP_SSL(work_smtp_server, 000) as server: # ❗000改为发邮件的SSL端口
        server.login(work_email, work_password)
        server.send_message(msg)
        server.close() # 发送完就关闭，避免报错

    print(f"邮件转发完成。")
    
except Exception as e:
    print(f"转发失败: {e}")