import os
from pathlib import Path

from celery import Celery

project = Path(__file__).parent.resolve().name
os.environ.setdefault("DJANGO_SETTINGS_MODULE", f"services_center.settings")

app = Celery(project)

app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.update(
    enable_utc=True,
    timezone="Asia/Shanghai"
)

app.conf.beat_schedule = {
    'loop-every': {
        'task': 'loop_ping_pong',
        'schedule': 180,
        'args': ()
    },
}
