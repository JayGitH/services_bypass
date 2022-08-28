from rest_framework.views import APIView
from django.http import JsonResponse

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
