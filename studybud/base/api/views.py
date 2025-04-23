from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import Room
from .serializers import RoomSerializer

# if we want to add delete then we can add like this
# @api_view(['GET','PUT','POST','DELETE'])

@api_view(['GET'])
def getRoutes(request):
    routes=[
        'GET /api',
        'GET /api/rooms',
        'GET /api/rooms/:id',
    ]

    # return JsonResponse(routes, safe=False)  #safe=False means we can return any data type, not just dictionaries
    return Response(routes)  #this will return a JSON response with the routes

@api_view(['GET'])
def getRooms(request):
    rooms = Room.objects.all()  #it is python list of objects
    serializer = RoomSerializer(rooms, many=True)  #many means we are serializing a list of objects
    return Response(serializer.data) 


@api_view(['GET'])
def getRoom(request, pk):
    room = Room.objects.get(id=pk)
    serializer = RoomSerializer(room, many=False)
    return Response(serializer.data)






#response cannot be serialized directly to JSON format Use the `RoomSerializer` to convert the Room objects to a JSON-serializable format.

#dictionary can be serialized directly to JSON format