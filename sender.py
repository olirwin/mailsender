import datetime
import logging
import smtplib
import imaplib
import ssl
import glob
import time

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

from email.utils import formatdate
from email import message_from_file
from pathlib import Path


logger = logging.getLogger("mail-sender")
formatter = logging.Formatter(
    fmt="%(asctime)s\t%(levelname)s\t%(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
handler = logging.FileHandler(Path("mail-sender.log"))
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)


USER = ""
PASSWORD = ""


def send_mails(files_dir: Path,
               attachment: Path = None):
    # Get all email files
    files = glob.glob(f"{files_dir}/*")

    # Construct email messages
    emails = []

    for file in files:
        with open(file=file, mode="r") as f:
            tmp = message_from_file(f)

        msg = MIMEMultipart()
        for k in tmp.keys():
            msg[k] = tmp[k]

        msg["Date"] = formatdate(localtime=True)

        msg.attach(MIMEText(tmp.get_payload(), _subtype="plain", _charset="utf-8"))

        # Add attachment if exists
        if attachment:
            with open(file=f"{attachment}", mode="rb") as f:
                attch = MIMEApplication(
                    f.read(),
                    _subtype="pdf",
                    Name=f"{attachment}"
                )

            attch.add_header(
                "Content-Disposition",
                "attachment",
                filename=f"{attachment}"
            )

            attch.add_header(
                "Content-ID",
                f"{attachment.name}"
            )

            msg.attach(attch)
        emails.append(msg)

    # Send email
    context = ssl.create_default_context()
    imap = imaplib.IMAP4_SSL("imap.univ-lille.fr", 993)
    imap.login(USER, PASSWORD)

    with smtplib.SMTP_SSL(
            host="smtp.univ-lille.fr",
            port=465,
            context=context
    ) as s:
        s.login(USER, PASSWORD)
        for msg in emails:
            logger.info(f"Sending to {msg['To']}")
            s.sendmail(msg["From"], msg["To"], msg.as_string())
            imap.append('Sent', '\\Seen', imaplib.Time2Internaldate(time.time()), msg.as_string().encode("utf-8"))

    imap.logout()

    print("Done")
