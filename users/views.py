from django.db.models import Q
# Create your views here.
from rest_framework import pagination
from rest_framework import status
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.serializers import ValidationError

from .models import User
from .serializers import UserSerializer
from django.shortcuts import render


class StandardResultsSetPagination(pagination.PageNumberPagination):
    # modify the default pagination style
    page_size = 5  # set the page size to 5
    page_size_query_param = 'limit'
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response(data)


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny, ]
    pagination_class = StandardResultsSetPagination
    lookup_field = 'id'
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer
    http_method_names = ['options', 'get', 'post', 'put', 'patch', 'delete']

    def get_queryset(self):
        queryset = User.objects.all()
        ordering = self.request.query_params.get("sort")
        name = self.request.query_params.get("name")
        if name:
            queryset = queryset.filter(
                Q(first_name__icontains=name)
                | Q(last_name__icontains=name)

            )
        age = self.request.query_params.get('age')
        if age:
            queryset = queryset.filter(age=age)
        if self.get_query_prams():
            queryset = queryset.filter(**self.get_query_prams())

        if ordering:
            ordering_field = ordering.replace('-', '')
            if ordering_field not in [f.name for f in User._meta.fields]:
                raise ValidationError(" '%s' field is not an valid option for sort" % ordering)
            queryset = queryset.order_by(ordering)
        return queryset

    def get_query_prams(self):
        """
        dynamic create a query dict on field name search
        eg. {'city__icontains': 'Baltimore'}
        :return: query_dict
        """
        fields = ['id', 'first_name', 'last_name', 'company_name', 'city',
                  'state', 'zip', 'email', 'web']
        query_params = self.request.query_params
        query_dict_keys = query_params.dict().keys()
        query_dict_keys = [field for field in query_dict_keys if field in fields]
        pram_dict = {}
        for query in query_dict_keys:
            value = self.request.query_params.get(query)
            if value:
                pram_dict.update({query + '__icontains': value})
        return pram_dict

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        response_data = {}  # serializer.data
        return Response(data=response_data, status=status.HTTP_201_CREATED, headers=headers)


def home(request):
    return render(request,template_name='home.html')