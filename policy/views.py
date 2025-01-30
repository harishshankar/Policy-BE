from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from policy.responce import ApiResponse
from .models import Policy
from .serializers import PolicySerializer
from django.db.models import Q

# Create your views here.


class PolicyViewList(APIView):
    """
    APIView for Policy List
    """

    def get(self, request):
        search = request.query_params.get("search", None)

        min_premium = request.query_params.get("min_premium", None)
        max_premium = request.query_params.get("max_premium", None)
        policy_type = request.query_params.get("policy_type", "").strip()
        min_coverage = request.query_params.get("min_coverage", None)

        sort_by = request.query_params.get("sort_by", None)  # -created_at

        policies = Policy.objects.all()

        if search:
            policies = policies.filter(Q(name__icontains=search))

        if min_premium:
            policies = policies.filter(premium__gte=min_premium)
        if max_premium:
            policies = policies.filter(premium__lte=max_premium)
        if policy_type:
            policies = policies.filter(type=policy_type)
        if min_coverage:
            policies = policies.filter(coverage__gte=min_coverage)

        if sort_by:
            policies = policies.order_by(sort_by)

        serializer = PolicySerializer(policies, many=True)

        additional_data = {"sort_by": sort_by}
        return ApiResponse.success(
            serializer.data,
            status=status.HTTP_200_OK,
            additional_data=additional_data,
            request=request,
        )

    """
    API View for Policy Create
    """

    def post(self, request):
        serializer = PolicySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PolicyViewDetail(APIView):
    """
    API View for Policy Detail
    """

    def get(self, request, pk):
        policy = Policy.objects.get(pk=pk)
        serializer = PolicySerializer(policy)
        return Response(serializer.data)

    """
    API View for Policy Update
    """

    def put(self, request, pk):
        policy = Policy.objects.get(pk=pk)
        serializer = PolicySerializer(policy, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    """
    API View for Policy Delete
    """

    def delete(self, request, pk):
        policy = Policy.objects.get(pk=pk)
        policy.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
