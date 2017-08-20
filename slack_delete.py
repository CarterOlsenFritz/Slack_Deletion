
#This script grabs X files up to a count limit then deletes them where Days are older than Y.
#It would be wise to add filters for which type of files we want to delete.
from credentials_slack import *
from urllib.parse import urlencode
from urllib.request import urlopen
import time
import json
import codecs

reader = codecs.getreader("utf-8")

#Token is issued from Slack at https://api.slack.com/custom-integrations/legacy-tokens
#I have stored the tokens in credentials_slack.py, which will not be hosted online anywhere.
token = token_alex


#Delete files older than this:
days = 30
ts_to = int(time.time()) - days * 24 * 60 * 60

def list_files():
  params = {
    'token': token,
    'ts_to': ts_to,
    'count': 1000,
  }
  uri = 'https://slack.com/api/files.list'
  response = reader(urlopen(uri + '?' + urlencode(params)))
  return json.load(response)['files']

def delete_files(file_ids):
  count = 0
  num_files = len(file_ids)
  for file_id in file_ids:
    count = count + 1
    params = {
      'token': token
      ,'file': file_id
      }
    uri = 'https://slack.com/api/files.delete'
    response = reader(urlopen(uri + '?' + urlencode(params)))
    print(count, "of", num_files, "-", file_id, json.load(response)['ok'])

files = list_files()
file_ids = [f['id'] for f in files]
delete_files(file_ids)