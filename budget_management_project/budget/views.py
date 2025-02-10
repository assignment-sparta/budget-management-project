from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status


from budget_management_project.expense.models import Category
from .models import Budget
from .serializers import CategorySerializer, BudgetSerializer


'''
카테고리 관관APIView
'''
class CategoryView(APIView):
    # 로그인한 사용자만 접근 가능
    permission_classes = [IsAuthenticated] #AllowAny
    
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


'''
예산 설정 APIView
'''
class BudgetView(APIView):
    # 로그인한 사용자만 접근 가능
    permission_classes = [IsAuthenticated] #AllowAny
    
    '''
    예산 목록 조회
    '''
    def get(self, request):
        # 현재 사용자의 예산 목록 조회
        budgets = Budget.objects.filter(user=request.user) # budgets = Budget.objects.all()
        serializer = BudgetSerializer(budgets, many=True)
        return Response({
            "message": "예산 목록 조회 성공",
            "data": serializer.data
        }, status=status.HTTP_200_OK)


    '''
    예산 설정
    '''
    def post(self, request):
        # request.data에 user 정보 추가
        data = request.data.copy()
        data['user'] = request.user.id
        
        serializer = BudgetSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "예산 설정 성공",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
            
        return Response({
            "message": "예산 설정 실패",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
