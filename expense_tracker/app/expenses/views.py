from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from expense_tracker.app.expenses.models import Expense
from expense_tracker.app.expenses.serializers import (
  ExpenseSerializer,
  ExpenseDetailSerializer
)
from expense_tracker.util.permissions import IsOwner
from expense_tracker.util.renderers import ResponseRenderer



class ExpenseAPIViewSet(viewsets.ModelViewSet):
  queryset = Expense.objects.all()
  serializer_class = ExpenseDetailSerializer
  permission_classes = [IsAuthenticated, IsOwner]
  lookup_field = 'pk'
  renderer_classes = [ResponseRenderer]
  
  def perform_create(self, serializer):
    serializer.save(owner=self.request.user)
  
  def get_queryset(self):
    return self.queryset.filter(owner=self.request.user).order_by('-id')
  
  def get_serializer_class(self):
    if self.action == 'list':
      return ExpenseSerializer
    return self.serializer_class
