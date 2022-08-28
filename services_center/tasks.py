from services_bypass.celery import app


@app.task(name='loop_ping_pong')
def loop_query_task():
    ...
