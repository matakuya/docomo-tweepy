#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import urllib.request
import json
import logging
import configparser

class DocomoIface(object):
  def __init__(self):
    config = configparser.ConfigParser()
    config.read('settings.conf')
    BASE_URL = config['docomo']['base_url']
    API_KEY = config['docomo']['api_key']
    self.__uri = "{}/?APIKEY={}".format(BASE_URL, API_KEY)
    self.__method = "POST"
    self.__headers = {"Content-Type" : "application/json"}

  def send_msg(self, message):
    req_body = {"utt": message}
    json_data = json.dumps(req_body).encode("utf-8")
    req = urllib.request.Request(self.__uri, data=json_data, headers=self.__headers, method=self.__method)
    try:
      res = urllib.request.urlopen(req)
    except Exception as e:
      logging.error(e)
      sys.exit()
    with res as r:
      st = r.read().decode('utf-8')
      res_json = json.loads(st)
      logging.debug(res_json['utt'])
      return res_json['utt']

if __name__ == '__main__':
  docomo = DocomoIface()
  res = docomo.send_msg("おはようございます")
  print(res)
