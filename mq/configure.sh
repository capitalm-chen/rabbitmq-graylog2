#!/bin/sh

add_user() {
  user="$1"
  pass="$2"

  # `graylog []`
  rabbitmqctl list_users | grep "^$user\\s" >/dev/null \
    || rabbitmqctl add_user "$user" "$pass"

  # `/       log-messages    log-messages    log-messages`
  rabbitmqctl list_user_permissions "$user" \
    | grep "^/\s$3\s$4\s$5" >/dev/null \
    || rabbitmqctl set_permissions -p / "$user" "$3" "$4" "$5"
}

add_user graylog graylog log-messages log-messages log-messages
add_user mqtt mqtt 'mqtt-subscription-paho/.*' 'amq.topic|log\..*' ''
