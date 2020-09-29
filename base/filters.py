import django_filters
from django_filters import CharFilter

from django import forms

from .models import *

class ProductFilter(django_filters.FilterSet):
	name = CharFilter(field_name='name', lookup_expr="icontains", label='Product Name')
	# tags = django_filters.ModelMultipleChoiceFilter(queryset=Tag.objects.all(),
	# 	widget=forms.CheckboxSelectMultiple
	# 	)
	class Meta:
		model = Product
		fields = ['name']


class CategoryFilter(django_filters.FilterSet):
	name = CharFilter(field_name='name', lookup_expr="icontains", label='Category Name')
	# tags = django_filters.ModelMultipleChoiceFilter(queryset=Tag.objects.all(),
	# 	widget=forms.CheckboxSelectMultiple
	# 	)
	class Meta:
		model = Category
		fields = ['name']