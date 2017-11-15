from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import ReceivedData, SentData

from .serializers import *
from rest_framework import status , generics , mixins
from django.db import connection

# Create your views here.
def home_view(request):
	template_name='home.html'
	context={'hosts':[20,20,20,30,50]}
	return render(request,template_name,context)

def host_view(request,host_name):
	template_name='host.html'
	context={'host':host_name}
	return render(request,template_name,context)
	
@api_view(['GET', 'POST'])
def sent_data(request):
    """
    List all SentData, or create a new SentData.
    """
    print(request.method)
    if request.method == 'GET':
        sentData = SentData.objects.all()
        serializer = SentDataSerializer(sentData,context={'request': request} ,many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = SentDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def received_data(request):
    """
    List all ReceivedData, or create a new ReceivedData.
    """
    print(request.method)
    if request.method == 'GET':
        receivedData = ReceivedData.objects.all()
        serializer = ReceivedDataSerializer(receivedData,context={'request': request} ,many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ReceivedDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def sent_data_detail(request, pk):
    """
    Retrieve, update or delete a SentData instance.
    """
    try:
        sentData = SentData.objects.get(pk=pk)
        print(sentData)
    except SentData.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SentDataSerializer(sentData,context={'request': request})
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = SentDataSerializer(sentData, data=request.data,context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        sentData.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'PUT', 'DELETE'])
def received_data_detail(request, pk):
    """
    Retrieve, update or delete a ReceivedData instance.
    """
    try:
        receivedData = ReceivedData.objects.get(pk=pk)
        print(receivedData)
    except ReceivedData.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ReceivedDataSerializer(receivedData,context={'request': request})
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ReceivedDataSerializer(receivedData, data=request.data,context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        receivedData.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
