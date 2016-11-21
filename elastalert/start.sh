#!/bin/sh

/wait-for-it.sh elasticsearch:9200 --timeout=0

cd /etc/elastalert

elastalert-create-index --index elastalert_status --old-index None

/usr/local/bin/elastalert --config /etc/elastalert/config.yaml --verbose
