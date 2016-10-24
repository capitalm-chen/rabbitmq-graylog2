#!/bin/sh

SCRIPT_ROOT=`dirname "$0"`

cd "$SCRIPT_ROOT"

for container in `docker-compose ps -q mq`; do
  docker exec -i -t $container sh /configure.sh
done

echo "Creating exchange: log-messages"
curl -o /dev/null -X PUT -H 'Content-Type: application/json' \
       -d "`cat $SCRIPT_ROOT/mq/log-messages`" \
       'http://mq-admin:mq-password@localhost:15672/api/exchanges/%2F/log-messages'

echo "Binding exchange"
curl -o /dev/null -X POST -H 'Content-Type: application/json' \
      -d "`cat $SCRIPT_ROOT/mq/bindings`" \
      'http://mq-admin:mq-password@localhost:15672/api/bindings/%2F/e/amq.topic/e/log-messages'

python "$SCRIPT_ROOT/graylog2/configure.py"
