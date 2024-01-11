from django.shortcuts import render

from .models import Profile, User, ChatMessage
from .serializer import UserSerializer, MyTokenObtainPairSerializer, RegisterSerializer, MessageSerializer

from rest_framework.decorators import api_view, permission_classes
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework.views import APIView
import json
from django.db.models import Subquery, OuterRef, Q
from django.db import connection

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer


# @api_view(["GET","POST"])
# @permission_classes([IsAuthenticated])
# def dashboard(request):
#     if request.method == "GET":
#         context = f"Hey {request.user}, You are seeing get response."
#         return Response({"response": context}, status=status.HTTP_200_OK)
#     elif request.method == "POST":
#         text = request.POST.get('text')
#         context = f"Hey {request.user}, Your text is: {text}."
#         return Response({"response": context}, status=status.HTTP_200_OK)
    
#     return Response({}, status=status.HTTP_400_BAD_REQUEST)

@permission_classes([IsAuthenticated])
class DashboardView(APIView):
    def get(self, request):
        context = f"Hey {request.user}, You are seeing get response."
        return Response({"response": context}, status=status.HTTP_200_OK)
    
    def post(self, request):
        text = request.POST.get('text')
        context = f"Hey {request.user}, Your text is: {text}."
        return Response({"response": context}, status=status.HTTP_200_OK)
    

class MyInbox(generics.ListAPIView):
    serializer_class=MessageSerializer
    
    def get_queryset(self):
        user_id = self.kwargs["user_id"]
        
        messages = ChatMessage.objects.filter(
            id__in = Subquery(
                User.objects.filter(
                    Q(sender__receiver=user_id) | 
                    Q(receiver__sender=user_id)
                ).distinct().annotate(
                    last_msg = Subquery(
                        ChatMessage.objects.filter(
                            Q(sender=OuterRef("id") , receiver=user_id) |
                            Q(receiver=OuterRef("id") , sender=user_id)
                        ).order_by("-id")[:1].values_list("id", flat=True)
                    )
                ).values_list("last_msg", flat=True).order_by("-id")
            )
        ).order_by("-id")
        
        print(messages)
        print(connection.queries)
        return messages

