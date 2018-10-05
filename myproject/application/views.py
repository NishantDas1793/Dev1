from django.shortcuts import render, get_object_or_404
from .models import People, Address
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.core import serializers
import json
from rest_framework import generics
from .permission import IsOwnerOrReadOnly
from .serializers import peopleSerializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
import threading

# Create your views here.

def home(request):
    data = People.objects.all()
    query = request.GET.get('q')
    if query:
        data = data.filter(Q(Name__iexact=query) | 
            Q(age__icontains=query) | 
            Q(email__icontains=query) | 
            Q(sex__icontains=query) | 
            Q(height__icontains=query) | 
            Q(weight__icontains=query) | 
            Q(address__State__icontains=query) | 
            Q(relationship__icontains=query))
    # data_serialized = serializers.serialize('json', data)
    # return JsonResponse(data_serialized, safe=False)
    return render(request, 'home.html', {'data': data})

@api_view(['GET',])
def male(request):
    people = People()
    people = people.male()
    serializer = peopleSerializers(people, many=True)
    # import IPython; IPython.embed();
    return Response(serializer.data)

    # data = data.male()[0].Name
    # data_serialized = serializers.serialize('json', data)
    # return JsonResponse(data_serialized, safe=False)

class PeopleListView(generics.ListAPIView):
    lookup_field = 'pk'
    serializer_class = peopleSerializers

    def get_queryset(self):
        data = People.objects.all()
        query = self.request.GET.get('q')
        if query:
            data = data.filter(Q(Name__icontains=query) | 
                Q(age__icontains=query) | 
                Q(email__icontains=query) | 
                Q(sex__icontains=query) | 
                Q(height__icontains=query) | 
                Q(weight__icontains=query) | 
                Q(address__State__icontains=query) | 
                Q(relationship__icontains=query))
        return data


# class PeopleCreateView(generics.CreateAPIView):
#     lookup_field = 'pk'
#     serializer_class = peopleSerializers
#     # permission_classes = [IsOwnerOrReadOnly]


# Function based views

@api_view(["POST"])
def people_create(request):
    serializer = peopleSerializers(data = request.data)
    # import IPython; IPython.embed();
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "People Created"}, status=200)
    else:
        data = {
        "error": True,
        "errors": serializer.errors,          
        }
        return Response(data, status=400)


@api_view(["GET"])
def people_list(request):
    people = People.objects.all()
    serializer = peopleSerializers(people, many=True)
    return Response(serializer.data)

@api_view(["GET"])
def people_detail(request, pk):
    people = get_object_or_404(People, pk=pk)
    serializer = peopleSerializers(people)
    return Response(serializer.data)

@api_view(["GET", "PUT"])
def people_update(request, pk):
    people = get_object_or_404(People, pk=pk)
    if request.method == "PUT":
        serializer = peopleSerializers(people, data=request.data)
        # import IPython; IPython.embed();
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        else:
            return Response({"error": serializer.errors, "error": True})
    # import IPython; IPython.embed();
    serializer = peopleSerializers(people)
    return Response(serializer.data)

def delete_people(request, pk):
    people = get_object_or_404(People, pk=pk)
    people.delete()
    return JsonResponse({"message": "Deleted"})




def print_cube(num): 
    print("Cube: {}".format(num * num * num)) 
  
def print_square(num): 
    print("Square: {}".format(num * num)) 
  
def main():  
    t1 = threading.Thread(target=print_square, args=(10,)) 
    t2 = threading.Thread(target=print_cube, args=(10,)) 

    t1.start()

    t2.start() 

    # t1.join()
    # t2.join() 
    return JsonResponse({'message': 'main_run'}) 