from django.db import transaction
from rest_framework import generics, status
from rest_framework.response import Response

from expense.serializers import ExpenseSerializer
from expense.permissions import IsExpenseOwner

class ExpenseCreateView(generics.CreateAPIView):
    serializer_class = ExpenseSerializer
    permission_classes = [IsExpenseOwner]

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response({
            'message': '지출이 성공적으로 생성되었습니다.',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)


class ExpenseUpdateView(generics.UpdateAPIView):
    serializer_class = ExpenseSerializer
    permission_classes = [IsExpenseOwner]