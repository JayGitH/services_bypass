import time, os
from concurrent.futures import ThreadPoolExecutor

from services_bypass.celery import app
from .models import Service

import httpx

TIMES = 3
# 线程执行池
executor = ThreadPoolExecutor(max_workers=os.getenv('MAX_WORKERS', 8))


# 心跳检测
def try_ping_pong_times(service: Service):
    count = 0
    while count < TIMES:
        r = httpx.get(f'{service.server()}/ping')
        try:
            assert r.status_code == 200
            assert r.json()['result'] == 'pong'
            return
        except Exception as e:
            if count <= TIMES:
                print(f'第{count + 1}次心跳检测: 失败')
                time.sleep(10)
            else:
                print(f"{service.name}服务丢失: {e}")
                service.delete()

        count += 1


@app.task(name='loop_ping_pong')
def loop_query_task():
    services = Service.objects.all()
    executor.map(try_ping_pong_times, services)
