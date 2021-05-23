import django_filters
from django.db.models import Q
from .models import *

class RegistrationFilter(django_filters.FilterSet):
    student_id = django_filters.CharFilter(field_name='student_id__student__username', lookup_expr='icontains')
    class Meta:
        model = Students_registration
        fields = '__all__'
        exclude = ['id', 'supervisor_id', 'agreement', 'reject_reason', 'created_at', 'updated_at', 'objects']


class ReportFilter(django_filters.FilterSet):
    student_id = django_filters.CharFilter(field_name='student_id__student__username', lookup_expr='icontains')
    class Meta:
        model = Report_submitting
        fields = '__all__'
        exclude = ['id', 'report_id', 'references', 'grade', 'created_at', 'updated_at', 'objects']

class StudentFilter(django_filters.FilterSet):
    student_id = django_filters.CharFilter(field_name='student__username', lookup_expr='icontains')
    class Meta:
        model = Students
        fields = '__all__'
        exclude = ['id', 'gender', 'display_image', 'address', 'created_at', 'updated_at', 'objects']

class CompanyFilter(django_filters.FilterSet):
    company_id = django_filters.CharFilter(field_name='company__username', lookup_expr='icontains')
    class Meta:
        model = Company
        fields = '__all__'
        exclude = ['id', 'gender', 'display_image', 'in_whitelist', 'address', 'created_at', 'updated_at', 'objects']

class StaffFilter(django_filters.FilterSet):
    staff_id = django_filters.CharFilter(field_name='staff__email', lookup_expr='icontains')
    class Meta:
        model = Staffs
        fields = '__all__'
        exclude = ['id', 'gender', 'display_image', 'address', 'created_at', 'updated_at', 'objects']