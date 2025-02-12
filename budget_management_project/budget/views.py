from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from budget_management_project.budget.models import Budget
from budget_management_project.budget.serializers import BudgetSerializer


class BudgetView(APIView):
    '''
    예산 설정 APIView
    '''
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        '''
        예산 목록 조회
        '''
        budgets = Budget.objects.filter(user=request.user)
        serializer = BudgetSerializer(budgets, many=True)
        return Response({
            "message": "예산 목록 조회 성공",
            "data": serializer.data
        }, status=status.HTTP_200_OK)


 
    def post(self, request):
        '''
        예산 설정
        '''
        serializer = BudgetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({
                "message": "예산 설정 성공",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
            
        return Response({
            "message": "예산 설정 실패",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
