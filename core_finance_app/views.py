from rest_framework import viewsets
from .serializers import IncomeSerializer
from .models import Income

class IncomeViewSet(viewsets.ModelViewSet):
    queryset = Income.objects.all()
    serializer_class = IncomeSerializer
