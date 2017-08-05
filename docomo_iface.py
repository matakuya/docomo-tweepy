#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import urllib.request
import json

APP_URL = "https://api.apigw.smt.docomo.ne.jp/dialogue/v1/dialogue"
API_KEY = "5232394162636b647a47526b303639493647314b62466f313532626c522e674f687234766f396679687843"

class DocomoIface(object):
  def __init__(self, api_key=API_KEY):
    self.uri = "{}/?APIKEY={}".format(APP_URL, API_KEY)
    self.method = "POST"
    self.headers = {"Content-Type" : "application/json"}
    print(self.uri)

  def send_msg(self, message):
    req_body = {"utt": message}
    json_data = json.dumps(req_body).encode("utf-8")
    req = urllib.request.Request(self.uri, data=json_data, headers=self.headers, method=self.method)
    try:
      #res = urllib.request.urlopen(req)
      res = urllib.request.urlopen(req)
    except Exception as e:
      print(e)
      sys.exit()
    with res as r:
      st = r.read().decode('utf-8')
      res_json = json.loads(st)
      return res_json['utt']


if __name__ == '__main__':
  docomo = DocomoIface()
  res = docomo.send_msg("こんばんは")
  print(res)

