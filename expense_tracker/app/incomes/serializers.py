from rest_framework import serializers
from expense_tracker.app.incomes.models import Income


class IncomeSerializer(serializers.ModelSerializer):
  class Meta:
    model = Income
    fields = ['id', 'source', 'amount', 'date']
    read_only_fields = ['id']

    
class IncomeDetailSerializer(IncomeSerializer):
  class Meta(IncomeSerializer.Meta):
    fields = IncomeSerializer.Meta.fields + ['description']