#!/usr/bin/env python

import urllib2
import json


class GraylogConfigure(object):
    GRAYLOG_HOST = 'localhost'
    GRAYLOG_PORT = 9000
    GRAYLOG_USER = 'admin'
    GRAYLOG_PASSWORD = 'graylog-password'

    def __init__(self):
        auth_handler = urllib2.HTTPBasicAuthHandler()
        host = '%s:%d' % (self.GRAYLOG_HOST, self.GRAYLOG_PORT)
        auth_handler.add_password('Graylog Server', host, self.GRAYLOG_USER, self.GRAYLOG_PASSWORD)
        opener = urllib2.build_opener(auth_handler)
        urllib2.install_opener(opener)
        self.url = 'http://%s' % (host,)

    def get(self, api):
        url = '%s%s' % (self.url, api)
        response = json.loads(urllib2.urlopen(url).read())
        print json.dumps(response, indent=2)
        return response

    def post(self, api, data):
        url = '%s%s' % (self.url, api)
        req = urllib2.Request(url, data=json.dumps(data),
                              headers={'Content-type': 'application/json'})
        urllib2.urlopen(req)

    def get_node_id(self):
        response = self.get('/api/system/cluster/nodes')
        if not response['nodes']:
            return None
        return response['nodes'][0]['node_id']

    def setup_input(self):
        input_ = self.get_input()
        if input_:
            return input_
        node_id = self.get_node_id()
        if not node_id:
            raise('Error getting node ID')
        self.add_input(node_id)
        return self.get_input()

    def get_input(self):
        response = self.get('/api/system/inputs')
        for input in response['inputs']:
            if input['title'] == 'mq':
                return input
        return None

    def add_input(self, node_id):
        print 'Adding graylog input: mq'
        data = {
            "title": "mq",
            "type": "org.graylog2.inputs.raw.amqp.RawAMQPInput",
            "configuration": {
                "throttling_allowed": False,
                "broker_hostname": "mq",
                "broker_port": 5672,
                "broker_vhost": "/",
                "broker_username": "graylog",
                "broker_password": "graylog",
                "prefetch": 100,
                "queue": "log-messages",
                "exchange": "log-messages",
                "exchange_bind": True,
                "routing_key": "#",
                "parallel_queues": 1,
                "heartbeat": 60,
                "tls": False,
                "requeue_invalid_messages": False,
                "override_source": None
            },
            "global": False,
            "node": node_id
        }
        self.post('/api/system/inputs', data)

    def setup_extractor(self, input_id):
        if not self.get_extractor(input_id):
            self.add_extractor(input_id)

    def get_extractor(self, input_id):
        url = '/api/system/inputs/%s/extractors' % (input_id,)
        response = self.get(url)
        for entry in response['extractors']:
            if entry['title'] == 'json':
                return entry
        return None

    def add_extractor(self, input_id):
        data = {
            'title': 'json',
            'cut_or_copy': 'copy',
            'source_field': 'message',
            'target_field': '',
            'extractor_type': 'json',
            'extractor_config': {
                'list_separator': ', ',
                'key_separator': '.',
                'kv_separator': '=',
                'key_prefix': '',
                'replace_key_whitespace': False,
                'key_whitespace_replacement': '_'
            },
            'converters': {},
            'condition_type': 'none',
            'condition_value': ''
        }
        url = '/api/system/inputs/%s/extractors' % (input_id,)
        self.post(url, data)

    def main(self):
        input_id = self.setup_input()['id']
        self.setup_extractor(input_id)


def main():
    configure = GraylogConfigure()
    configure.main()


if __name__ == '__main__':
    main()
