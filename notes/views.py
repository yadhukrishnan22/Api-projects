from django.shortcuts import render

from rest_framework import generics

from notes.serializers import UserSerializer, TaskSerializer

from notes.models import User, Task

from rest_framework.response import Response

from rest_framework import permissions, authentication

from notes.permissions import OwnerOnly

from rest_framework.views import APIView

from django.db.models import Count



class UserCreationView(generics.CreateAPIView):

    serializer_class = UserSerializer

    # def post(self, request, *args, **kwargs):

        # serializer_instance = UserSerializer(data = request.data)

        # if serializer_instance.is_valid():

        #     data = serializer_instance.validated_data

        #     # User.objects.create_user(**data)

        #     return Response(data = serializer_instance.data)
        
        # else:

        #     return Response(data = serializer_instance.errors)


class TaskCreateView(generics.ListCreateAPIView):

    serializer_class = TaskSerializer

    queryset = Task.objects.all()

    authentication_classes = [authentication.TokenAuthentication]

    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):

        return serializer.save(owner = self.request.user)
    
    def get_queryset(self):

        qs = Task.objects.filter(owner = self.request.user)

        if 'category' in self.request.query_params:

            cat_value = self.request.query_params.get('category')

            qs = qs.filter(category = cat_value)
        
        if 'priority' in self.request.query_params:

            priority_value = self.request.query_params.get('priority')

            qs = qs.filter(category = priority_value)


        return qs


class TaskRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = TaskSerializer

    queryset = Task.objects.all()

    authentication_classes = [authentication.TokenAuthentication]

    permission_classes = [OwnerOnly]
    

class TaskSummaryApiView(APIView):

    authentication_classes = [authentication.TokenAuthentication]

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):

        qs = Task.objects.filter(owner = request.user)

        summary = qs.values('category').annotate(count = Count('category') )

        priority = qs.values('priority').annotate(count = Count('priority'))

        status = qs.values('status').annotate(count = Count('status'))

        task_count = qs.count()

        context = {
            'summary': summary,
            'priority':priority,
            'status':status,
            'total':task_count
        }

        return Response(data = context)
    

class CategoryListApiView(APIView):

    def get(self, request, *args, **kwargs):

        qs = Task.category_choices

        st = {cat for tp in qs for cat in tp}

        return Response(data = st )
    



    





        

     
             



        



