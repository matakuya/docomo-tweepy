#!/usr/bin/env python
# coding: utf-8
import tweepy
import configparser
import re
import docomo_iface

config = configparser.ConfigParser()
config.read('settings.conf')

CONSUMER_KEY = config['tweepy']['cons_key']
CONSUMER_SECRET = config['tweepy']['cons_sec']
ACCESS_TOKEN_KEY = config['tweepy']['accto_key']
ACCESS_TOKEN_SECRET = config['tweepy']['accto_sec']

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)
print("OAuth done.")

class TweepyStreamListener(tweepy.StreamListener):
    def __init__(self):
        super().__init__()
        config = configparser.ConfigParser()
        config.read('settings.conf')
        self.user_id = config['tweepy']['user_id']
        self.docomo_iface = docomo_iface.DocomoIface()

    def on_status(self, status):
        # @screenname 最短一致
        pure_text = re.sub(r"@.*? ", "", status.text)
        reply_text = "@" + status.author.screen_name + " " + self.docomo_iface.send_msg(pure_text)
        print("----------------")
        print(status.author.screen_name)
        print(status.text)
        print(pure_text)
        if(status.in_reply_to_user_id_str == self.user_id):
            print('Received reply.')
            print(reply_text)
            print('Updated.')
            api.update_status(status=reply_text,in_reply_to_status_id=status.id)

    def on_error(self, status_code):
        if status_code == 420:
            print(str(status_code))
            return False

if __name__ == '__main__':
    stream = tweepy.Stream(auth, listener=TweepyStreamListener())
    print("Stream start.")
    # tp.stream.filter(track=['python'])
    stream.userstream()
