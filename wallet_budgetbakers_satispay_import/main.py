#!/usr/bin/python

import csv
import os
import sys

database = []


class Entry:
    def __init__(self, description, category, dateTime, value, currency):
        import arrow
        import datetime

        dateTime = arrow.get(dateTime, "D MMM YYYY, H:mm:ss", locale="it_IT")
        self.date = dateTime.strftime("%d-%m-%Y")
        self.time = dateTime.strftime("%H:%M")

        self.value = float(value)
        self.currency = currency

        self.beneficiary = description

        if category == "Person to Person":
            self.description = "Trasferimento a/da " + description
        elif category == "Customer to Business":
            self.description = "Pagamento a " + description
        elif category == "Bank":
            self.description = description
        else:
            self.description = ""

    def __repr__(self):
        return str(self.date)


def main():
    from tkinter import Tk
    from tkinter.filedialog import askopenfilename

    Tk().withdraw()
    filename = (
        askopenfilename()
    )
    print("File selected: " + filename + "\n")
    loadCSV(filename)
    writeCSV("output.csv")
    input("Press Enter to continue...")


def loadCSV(fileName):
    with open(fileName) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        line_count = 0
        for row in csv_reader:
            if line_count > 0:
                entry=Entry(row[1], row[3], row[4], row[5], row[6])
                database.append(entry)
                print(entry)
            line_count += 1


def writeCSV(fileName):
    with open(os.path.join(sys.path[0], fileName), mode="w", newline="") as csv_file:
        csv_writer = csv.writer(
            csv_file, delimiter=";", quotechar='"', quoting=csv.QUOTE_MINIMAL
        )
        csv_writer.writerow(
            ["date", "time", "description", "beneficiary", "value", "currency"]
        )
        for index in database:
            csv_writer.writerow(
                [
                    index.date,
                    index.time,
                    index.description,
                    index.beneficiary,
                    str(index.value),
                    index.currency,
                ]
            )


"""def mailSender(message):
    print(message)
    try:
        server = smtplib.SMTP(cfg["Email"]["smtpServer"],
                              cfg["Email"]["smtpPort"])
        server.ehlo()
        server.starttls()
        server.ehlo
        server.login(cfg["Email"]["user"], cfg["Email"]["password"])

        server.send_message(message)
        print("Mail sent")
    except:
        print('Something went wrong...')
        return
    finally:
        server.quit()"""


if __name__ == "__main__":
    main()
