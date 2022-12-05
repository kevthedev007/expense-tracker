from rest_framework import serializers
from expense_tracker.app.expenses.models import Expense


class ExpenseSerializer(serializers.ModelSerializer):
  class Meta:
    model = Expense
    fields = ['id', 'category', 'amount', 'date']
    read_only_fields = ['id']
    
    
class ExpenseDetailSerializer(ExpenseSerializer):
  class Meta(ExpenseSerializer.Meta):
    fields = ExpenseSerializer.Meta.fields + ['description']