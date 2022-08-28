from services_bypass.celery import app
from .models import Service

import httpx


# 心跳检测
def try_ping_pong_times(service: Service, times=3):
    count = 0
    while count < times:
        r = httpx.get(f'{service.server}/{service.pong}')
        try:
            assert r.status_code == 200
            return
        except Exception as e:
            if count <= times:
                print(f'第{count + 1}次心跳检测: 失败')
            else:
                print(f"{service.name}服务丢失: {e}")
                service.delete()

        count += 1


@app.task(name='loop_ping_pong')
def loop_query_task():
    for service in Service.objects.all():
        try_ping_pong_times(service)
