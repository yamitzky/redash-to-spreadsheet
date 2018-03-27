# redash-to-spreadsheet

Export Redash -> Spreadsheet, in private network

## Motivation

Tables in Redash can be accessible from Google Spreadsheet via `IMPORTDATA` if your Redash is in public network.

If your Redash is OSS version and hosted in private network, it cannot be accessible from Spreadsheet.

By running redash-to-spreadhseet in same private network, it dumps Redash result to Spreadsheet.

## Prepare environment variables

Set environment variables.

```
export OAUTH2_JSON_CREDENTIAL={"type": "service_account", ...}
export REDASH_URL=https://base.url.of.your.redash
export REDASH_API_KEY=blahblahblah
```

To get `OAUTH2_JSON_CREDENTIAL`, you can see [this guide](http://gspread.readthedocs.io/en/latest/oauth2.html).

`REDASH_API_KEY` must be [User API Key](https://help.redash.io/article/128-api-key-authentication).

## Prepare Spreadsheet

Create new spreadsheet prefixed with `Qxxx:`, e.g. `Q123: DAU table`). If your sheet's name is `Q123: DAU table`, query result with id `123` will be exported.
This name pattern can be configured by setting `SHEET_NAME_PATTERN`.

Then, add permission of the created service account `xxxxx@yyyyy.iam.gserviceaccount.com` to the sheet.

## Usage

Run `./redash-to-spreadsheet` or `docker run -it --rm --env-file .env yamitzky/redash-to-spreadhseet`.
