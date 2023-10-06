from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from .serializers import *
from .models import *

@api_view(['GET'])
def list_chat(request, my_id ,peer_id):
    messages = Message.objects.filter(peer_id=peer_id, my_id=my_id) | Message.objects.filter(peer_id=my_id, my_id=peer_id)
    messages = messages.order_by('date_added')
    serializer = MessageSerializer(messages, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def add_message(request):
    serializer = MessageSerializer(data=request.data)
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        print(serializer.errors)
        return Response('An error occured')
