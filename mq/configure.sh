#!/bin/sh

# `graylog []`
rabbitmqctl list_users | grep '^graylog\s' >/dev/null \
  || rabbitmqctl add_user graylog graylog

# `/       log-messages    log-messages    log-messages`
rabbitmqctl list_user_permissions graylog \
  | grep '^/\slog-messages\slog-messages\slog-messages' >/dev/null \
  || rabbitmqctl set_permissions -p / graylog log-messages log-messages log-messages
