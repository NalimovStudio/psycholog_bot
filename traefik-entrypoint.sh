#!/bin/sh
set -e

# Устанавливаем правильные права на acme.json
if [ -f /acme/acme.json ]; then
    chmod 600 /acme/acme.json
fi

# Запускаем оригинальную команду
exec "$@"