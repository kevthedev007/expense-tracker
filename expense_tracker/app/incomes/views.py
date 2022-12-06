from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from expense_tracker.app.incomes.models import Income
from expense_tracker.app.incomes.serializers import (
  IncomeSerializer,
  IncomeDetailSerializer
)
from expense_tracker.util.permissions import IsOwner
from expense_tracker.util.renderers import ResponseRenderer

# Create your views here.
class IncomeAPIViewSet(viewsets.ModelViewSet):
  queryset = Income.objects.all()
  serializer_class = IncomeDetailSerializer
  permission_classes = [ IsAuthenticated, IsOwner]
  lookup_field = 'pk'
  renderer_classes = [ResponseRenderer]
  
  def perform_create(self, serializer):
    serializer.save(owner=self.request.user)

  def get_queryset(self):
    return self.queryset.filter(owner=self.request.user).order_by('-id')
  
  def get_serializer_class(self):
    if self.action == 'list':
      return IncomeSerializer
    return self.serializer_class
  
  