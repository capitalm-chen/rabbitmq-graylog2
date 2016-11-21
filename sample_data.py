#!/usr/bin/env python

import paho.mqtt.publish as publish
from tzlocal import get_localzone
from datetime import datetime
import random
import json
import time


class Client(object):
    HOST = 'localhost'
    PORT = 1883
    AUTH = {'username': 'mqtt', 'password': 'mqtt'}

    @classmethod
    def publish(cls, topic, data):
        publish.single(topic=topic,
                       payload=json.dumps(data),
                       hostname=cls.HOST,
                       port=cls.PORT,
                       auth=cls.AUTH)


class Sample(object):
    def __init__(self, id='', type=''):
        self.id = id
        self.type = type
        self.data = {}

    def get(self):
        standard_data = {
            'source': {'id': self.id},
            'type': self.type,
            '@timestamp': self.get_time()
        }
        standard_data.update(self.data)
        return standard_data

    @staticmethod
    def get_time():
        local = get_localzone()
        return datetime.now(local).isoformat()

    def publish(self):
        topic = 'log.%s.%s' % (self.type, self.id)
        data = self.get()
        print 'publishing %s: %s' % (topic, data)
        Client.publish(topic, data)


class Sample1(Sample):
    def __init__(self):
        super(Sample1, self).__init__(id='2480300',
                                      type='huawei_E3131SignalStrength')

    def get(self):
        self.data = {
            'c8y_SignalStrength': {
                'ber': {
                    'unit': '%',
                    'value': random.uniform(0, 100)
                },
                'rssi': {
                    'unit': 'dBm',
                    'value': random.randrange(-80, 20, 1)
                }
            }
        }

        return super(Sample1, self).get()


class Sample2(Sample):
    def __init__(self):
        super(Sample2, self).__init__(id='1197500',
                                      type='queclink_GV200LocationUpdate')

    def get(self):
        self.data = {
            'text': 'Location updated',
            'c8y_Position': {
                'alt': random.uniform(0, 2000),
                'lng': random.uniform(-180, 180),
                'lat': random.uniform(-90, 90)
            }
        }

        return super(Sample2, self).get()


def main():
    random.seed()
    sample1 = Sample1()
    sample2 = Sample2()

    sample1.publish()
    time.sleep(1)
    sample2.publish()
    time.sleep(1)
    sample1.publish()
    time.sleep(1)
    sample2.publish()
    time.sleep(1)
    sample1.publish()
    time.sleep(1)
    sample2.publish()


if __name__ == '__main__':
    main()
