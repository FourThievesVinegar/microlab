#!/bin/bash

uwsgi -s /tmp/uwsgi-syringes.sock --plugin python --manage-script-name --mount /syringes=syringe_service:app --chmod-socket=666 --enable-threads &
uwsgi -s /tmp/uwsgi-stirrers.sock --plugin python --manage-script-name --mount /stirrers=stirrer_service:app --chmod-socket=666 &
uwsgi -s /tmp/uwsgi-heaters.sock --plugin python --manage-script-name --mount /heaters=heater_service:app --chmod-socket=666 --enable-threads --master &

