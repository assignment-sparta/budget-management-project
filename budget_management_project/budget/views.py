from django.shortcuts import render  
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status


from budget_management_project.expense.models import Category
from .serializers import CategorySerializer

#카테고리 관관APIView
class CategoryView(APIView):
    # 로그인한 사용자만 접근 가능
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # 모든 카테고리 조회
        categories = Category.objects.all()
        # CategorySerializer를 통해 데이터 직렬화
        serializer = CategorySerializer(categories, many=True)
        # 응답 반환
        return Response({
            "message": "카테고리 목록 조회 성공",
            "data": serializer.data
        }, status=status.HTTP_200_OK)
