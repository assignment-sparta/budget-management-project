from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from datetime import date
from .serializers import ExpenseSerializer
import calendar
from rest_framework.decorators import api_view
from .models import Expense, 
from expense.enums import CategoryType

# Create your views here.
class ExpenseAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        expense_serializer= ExpenseSerializer(data = request.data)
        if expense_serializer.is_valid():
            category_ids= [
                category.code for category in CategoryType
            ]
            
            # 아래와 같이 카테고리 나옵니다. 그리고 모델에 카테고리 정의해놓았던거 마이그레이션 파일에 보시면 
            # 참 쉽죠 이해하셨나요

            # 아래로 하게되면 category에 포함되어있는 Expense를 다가져올 수 있습니다.
            expenses = Expense.objects.filter(
                category_id__in=category_ids
            )# 네
            # 아래 SQL입니다. 준기님 이해되시죠
            # SELECT * FROM expense x -> expense라는 테이블에 * 모든 필드를 가져온다
            # WHERE x.category IN [1,2,3,4,5,6,7,8,9,10,11,12,13]; -> 이떄 카테고리는 in에 있는 값들을 참조하여 모두 가져온다.

            

            # [
            #     ('ETC', 1),
            #     ('TUITION_FEE', 2),
            #     ('BOOK_FEE', 3),
            #     ('COURSES_FEE', 4),
            #     ('COMMUNICATION_FEE', 5),
            #     ('FOOD_FEE', 6),
            #     ('TRANSPORTATION_FEE', 7),
            #     ('LEISURE_FEE', 8),
            #     ('SELF_DEVELOPMENT_FEE', 9),
            #     ('CLUB_FEE', 10),
            #     ('PREPARATION_FEE', 11),
            #     ('DORMITORY_FEE', 12),
            #     ('HEALTHCARE_FEE', 13)
            # ]

                        