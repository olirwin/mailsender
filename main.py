from pathlib import Path

import click
import six
from pyfiglet import figlet_format
from termcolor import colored

from generate_mustache import create_files
from sender import send_mails


def log(message, color, font="slant", figlet=False) -> None:
    if not figlet:
        six.print_(colored(message, color), flush=False)
    else:
        six.print_(colored(figlet_format(message, font=font), color), flush=False)


@click.command(name="MailSender", context_settings=dict(ignore_unknown_options=True))
@click.option("--template", "-t",
              default="template.mustache",
              help="Mustache template file")
@click.option("--data", "-d",
              default="data.csv",
              help="CSV data file")
@click.option("--tmp-dir",
              default="email",
              help="Temporary directory for emails")
@click.option("--delimiter",
              default=";",
              help="Input CSV delimiter")
@click.option("--id-col", "-id",
              default="last",
              help="Id column in the CSV")
@click.option("--attach", "-a",
              help="Attachment file")
@click.version_option(version="1.0.0")
def main(template: str,
         data: str,
         tmp_dir: str,
         delimiter: str,
         id_col: str,
         attach: str) -> None:
    log("MailSender CLI", color="blue", figlet=True)
    log("Welcome to MailSender", "green", font="bold")
    template = Path(template)
    data = Path(data)
    tmp_dir = Path(tmp_dir)
    if attach:
        attach = Path(attach)

    # Generate emails
    create_files(data_file=data, template=template, delimiter=delimiter, id_col=id_col, output_dir=tmp_dir)
    # Send emails
    send_mails(files_dir=tmp_dir, attachment=attach)


if __name__ == "__main__":
    main()
