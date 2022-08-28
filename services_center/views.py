from django.db.models import Q
from rest_framework.views import APIView
from django.http import JsonResponse

import httpx

from .models import Service


# 注册服务
class ServiceRegister(APIView):
    permission_classes = []

    @staticmethod
    def verify(request):
        try:
            assert 'name' in request.data
            assert 'server_host' in request.data
            assert 'server_port' in request.data
            return True, None
        except Exception as e:
            return False, str(e)

    def post(self, request):
        verify_result, result = self.verify(request)
        if not verify_result:
            return JsonResponse({'code': 0, 'result': f'字段不全: {result}'})

        if not (service := Service.objects.filter(
                name=request.data['name'],
                server_host=request.data['server_host'],
                server_port=request.data['server_port']
        ).first()):
            service = Service.objects.create(**request.data)

        return JsonResponse({'code': 1, 'result': service.pk})


# 查询服务
class ServiceListView(APIView):
    permission_classes = []

    @staticmethod
    def get(request):
        return JsonResponse({'code': 1, 'result': [
            service.serializer() for service in Service.objects.all()
        ]})


# 查询某个服务
class ServiceDetailView(APIView):
    permission_classes = []

    @staticmethod
    def get(request):
        service = Service.objects.filter(**request.query_params).first()
        return JsonResponse({'code': 1, 'result': None if service is None else service.serializer()})


# 服务端服务发现模式
class ServiceRequest(APIView):
    permission_classes = []

    @staticmethod
    def verify(request):
        try:
            assert 'host' in request.data
            assert 'method' in request.data
            assert 'api' in request.data
            assert 'data' in request.data

            return True, None
        except Exception as e:
            print(e)
            return False, str(e)

    def post(self, request):
        verify_result, result = self.verify(request)
        if not verify_result:
            return JsonResponse({'code': 0, 'result': result})

        q = Q(server_host=request.data['host'])
        if server_name := request.data.get('server_name'):
            q &= Q(server_name=server_name)

        if not (service := Service.objects.filter(q).first()):
            return JsonResponse({'code': 0, 'result': '未找到服务'})

        server = service.server()

        request_body = dict(url=f"{server}/{request.data['api']}")

        if header := request.data.get('header'):
            request_body['headers'] = header

        method = request.data['method'].upper()
        data = request.data['data']

        if method == 'GET':
            request_body['params'] = data
            r = httpx.get(**request_body)
        else:
            request_body['json'] = data
            r = httpx.post(**request_body)

        return JsonResponse({'code': 1, 'result': r.status_code})
