from django.db import models


# 服务模型
class Service(models.Model):
    name = models.CharField('服务名', max_length=128)
    server_name = models.CharField('域名', max_length=256, null=True)
    server_host = models.CharField('地址', max_length=16)
    server_port = models.CharField('端口', max_length=5)

    pong = models.CharField('心跳检测', max_length=256)

    def __str__(self):
        return f"<Service({self.pk}): {self.name}>"

    @property
    def server(self, ssl=True):
        return f"{'https' if ssl else 'http'}://{self.server_host}:{self.server_port}"
