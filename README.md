1. Install requirements
   ```bash
   pip install -r requirements.txt
   ```
2. Use `main.py`
   ```plain
    Usage: main.py [OPTIONS]
    
    Options:
      -t, --template TEXT  Mustache template file
      -d, --data TEXT      CSV data file
      --tmp-dir TEXT       Temporary directory for emails (Optional)
      --delimiter TEXT     Input CSV delimiter (DEFAULT : ';')
      -id, --id-col TEXT   Id column in the CSV
      -a, --attach TEXT    Attachment file (Optional)
      --version            Show the version and exit.
      --help               Show this message and exit.
   ```

Example mustache template given.

Example use:

```bash
$ python main.py --data qcm.csv --id-col last
```
will send emails to all people in `qcm.csv` using the `last` column as key.

For now attachments are the same for all emails.

