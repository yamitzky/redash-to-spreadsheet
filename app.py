import json
import re
import os

import gspread
import requests
from oauth2client.service_account import ServiceAccountCredentials

# TODO: logger


DEFAULT_SCOPES = 'https://spreadsheets.google.com/feeds,https://www.googleapis.com/auth/drive'

scopes = os.environ.get('OAUTH2_SCOPES', DEFAULT_SCOPES).split(',')
cred_dict = json.loads(os.environ['OAUTH2_JSON_CREDENTIAL'])
pattern = re.compile(os.environ.get('SHEET_NAME_PATTERN', '^Q(?P<query_id>\d+):'))
redash_api_key = os.environ['REDASH_API_KEY']
redash_url = os.environ['REDASH_URL']
encoding = os.environ.get('REDASH_CSV_WRITER_ENCODING', 'utf-8')


def dump():
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(cred_dict, scopes)
    client = gspread.authorize(credentials, gspread.client.Client)

    for sheet in client.openall():
        m = pattern.search(sheet.title)
        if not m:
            print(f'skip {sheet.title}')
            continue
        query_id = m.group('query_id')
        url = f"{redash_url}/api/queries/{query_id}/results.csv"
        print(f'fetching {url}')
        response = requests.get(url, {'api_key': redash_api_key})
        if not response.ok:
            print('response not ok')
            continue
        csv = response.text
        print(f'imported {sheet.title}')
        client.import_csv(sheet.id, csv.encode(encoding))
