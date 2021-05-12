import email
import smtplib
import configparser


def make_email_content(email_address):
    config = configparser.ConfigParser()
    config.read('settings.ini')
    text = config["EMAIL_CONTENT"]["greet"].format(name=email_address) + "\n\n" + config["EMAIL_CONTENT"]["greet"] + "\n\n" + config["EMAIL_CONTENT"]["body"].format(app_name=config["APP_INFO"]["name"])
    return text

def send_email(target_mail,subject,text):
    config = configparser.ConfigParser()
    config.read('settings.ini')
    PORT = config["EMAIL"]["PORT"]
    SERVER = config["EMAIL"]["SERVER"]
    FROM = config["EMAIL"]["FROM"]
    msg = email.message.EmailMessage()
    msg['From'] = FROM
    msg['To'] = target_mail
    msg['Subject'] = subject
    msg.set_content(text)

    # Send the mail
    server = smtplib.SMTP(SERVER)
    server.connect(SERVER, port=PORT)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(config["EMAIL"]["FROM"], config["EMAIL"]["PW"])
    server.sendmail(FROM, target_mail, msg.as_string())
    server.quit()
    return ""


if __name__ == '__main__':
    text =  """You have submitted a analysis to Damos Appos.
           Your task have been queued, when the result becomes 
           ready, you'll receive the results in this email address.
           
           Sincerely my app Team """
    send_email("","Confirmation of task initiation",text)
