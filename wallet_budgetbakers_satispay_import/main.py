#!/usr/bin/python

import csv
import os
import sys
import yaml
from datetime import datetime

config = None
database = []


class Entry:
    def __init__(self, description, dateTime, value, currency):
        import arrow
        import datetime

        dateTime = arrow.get(dateTime, "D MMM YYYY, H:mm:ss", locale="it_IT")
        self.date = dateTime.strftime("%d-%m-%Y")
        self.time = dateTime.strftime("%H:%M")

        self.value = float(value)
        self.currency = currency

        self.beneficiary = description

    def __repr__(self):
        return str(self.date + ", " + self.time + ", " + self.beneficiary + ", " + str(self.value) + ", " + self.currency)


def main():
    from tkinter import Tk
    from tkinter.filedialog import askopenfilename

    loadConfig()

    Tk().withdraw()
    filename = askopenfilename()
    print("File selected: " + filename + "\n")
    loadCSV(filename)

    outputFile = writeCSV(datetime.now().strftime("%Y%m%d") + "_output.csv")
    mailSender(outputFile)

    input("Press Enter to continue...")
    os.remove(outputFile)


def loadConfig():
    global config

    with open(os.path.join(sys.path[0], "config.yaml"), "r") as fileName:
        config = yaml.load(fileName, Loader=yaml.FullLoader)


def loadCSV(fileName):
    with open(fileName, newline='', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        line_count = 0
        for row in csv_reader:
            if line_count > 0:
                entry = Entry(row[1], row[4], row[5], row[6])
                database.append(entry)
                print(entry)
            line_count += 1


def writeCSV(fileName):
    filePath = os.path.join(sys.path[0], fileName)
    with open(filePath, mode="w", newline="") as csv_file:
        csv_writer = csv.writer(
            csv_file, delimiter=";", quotechar='"', quoting=csv.QUOTE_MINIMAL
        )
        csv_writer.writerow(
            ["date", "time", "beneficiary", "value", "currency"]
        )
        for index in database:
            csv_writer.writerow(
                [
                    index.date,
                    index.time,
                    index.beneficiary,
                    str(index.value),
                    index.currency,
                ]
            )

        return filePath


def mailSender(filePath):
    import smtplib
    from os.path import basename
    from email.mime.application import MIMEApplication
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    try:
        message = MIMEMultipart()
        message["From"] = config["senderAddress"]
        message["To"] = config["recipientAddress"]
        message["Subject"] = "Esportazione Satispay del " + datetime.now().strftime(
            "%d/%m/%Y"
        )

        attachment = MIMEText(open(filePath).read())
        attachment.add_header(
            "Content-Disposition", "attachment", filename=os.path.basename(filePath)
        )
        message.attach(attachment)

        server = smtplib.SMTP(config["smtpServer"], config["smtpPort"])
        server.ehlo()
        server.starttls()
        server.ehlo
        server.login(config["smtpUser"], config["smtpPassword"])

        server.sendmail(
            config["senderAddress"], config["recipientAddress"], message.as_string()
        )

        print("Mail sent")
    except:
        print("Something went wrong...")
        return
    finally:
        server.quit()


if __name__ == "__main__":
    main()
