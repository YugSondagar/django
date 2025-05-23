from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth import authenticate, login,logout
from django.http import HttpResponse
from . models import Room,Topic,Message,User
from . forms import RoomForm,MessageForm,UserForm,myuserCreationForm
from django.shortcuts import get_object_or_404

# rooms = [
#     {'id':1, 'name':'Lets learn python'},
#     {'id':2, 'name':'Design with me'},
#     {'id':3, 'name':'Frontend developers'},
# ]

def loginPage(request):
    page = 'login'
    
    #it will redirect me to home page if i am already logged in when i try to login
    if request.user.is_authenticated:
        return redirect('Home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        #to check if user exist
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')
        
        #if user exists then
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('Home')
        else:
            messages.error(request, 'Username or password does not exist')

    context = {'page':page}
    return render(request,'base/login_register.html',context)

def logoutUser(request):
    logout(request)
    return redirect('Home')

def registerUser(request):
    form = myuserCreationForm()

    if request.method == 'POST':
        form = myuserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False) #what does commit=Flase does it will freeze the form that means we want to access the user that was created right away
            user.username = user.username.lower()
            user.save()
            login(request,user)
            return redirect('Home')
        else:
            messages.error(request, 'An error occurred during registration')

    return render(request,'base/login_register.html',{'form':form})


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    # rooms = Room.objects.filter(topic__name__icontains=q)   #here we are only getting the rooms that match the query but we want it dynamic which means we can search user or room to get info
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q) 
    )


    topics = Topic.objects.all()[0:5]  # that will only give us 5 topics and the rest will be in more
    room_count = rooms.count()
    room_messages = Message.objects.filter( Q (room__topic__name__icontains=q)
    )

    context = {'rooms':rooms,'topics':topics,'room_count':room_count,'room_messages':room_messages}
    return render(request,'base/home.html',context)

def room(request,pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()  #here message is model but usko hamesha small se likhna hai. It will get all the messages associated with that room. FOR MANY TO ONE RELATIONSHIP WE WILL DO message_set.all()
    participants = room.participants.all() #this will get all the users who are in that room. FOR MANY TO MAN WE WILL DO participants.all()

    if request.method == 'POST':
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )
        room.participants.add(request.user) #this will add the user to the room.
        return redirect('Room',pk=room.id)

    context = {'room':room, 'room_messages':room_messages,'participants':participants}
    return render(request,'base/room.html',context)


def userProfile(request,pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context={'user':user,'rooms':rooms,'room_messages':room_messages,'topics':topics}
    return render(request,'base/profile.html',context)




@login_required(login_url='login')
def create_room(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        Room.objects.create(
            host = request.user,
            topic = topic,
            name = request.POST.get('name'),
            description = request.POST.get('description'),  
        )
        # form = RoomForm(request.POST)
        # if form.is_valid():
        #     room = form.save(commit = False) #When you use commit=False, Django creates the model instance but does NOT save it to the database yet. This allows you to modify the instance before saving.
        #     room.host = request.user
        #     room.save()
        return redirect('Home')
    context = {'form':form,'topic':topics}
    return render(request,'base/room_form.html',context)


@login_required(login_url='login')
def update_room(request,pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)  #it will make sure that the room has prewritten values with it
    topics = Topic.objects.all()

    #tum koi room ko update tabhi kar sakte ho jab tum room ka owner ho
    if request.user != room.host:
        return HttpResponse('You are not the owner of this room')

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        # form = RoomForm(request.POST, instance=room)  #why instance=room bcoz we need to tell him that we need to update that room or else he will create a new room
        # if form.is_valid():
        #     form.save()
        return redirect('Home')

    context = {'form':form,'topics':topics,'room':room}
    return render(request,'base/room_form.html',context)


@login_required(login_url='login')
def delete_room(request,pk):
    room = Room.objects.get(id=pk)

    #tum koi room ko delete tabhi kar sakte ho jab tum room ka owner ho
    if request.user != room.host:
        return HttpResponse('You are not the owner of this room')
    if request.method == 'POST':
        room.delete()
        return redirect('Home')
    
    return render(request,'base/delete.html',{'obj':room})


@login_required(login_url='login')
def Edit_message(request, pk):
    message = Message.objects.get(id=pk)
    form = MessageForm(instance=message)

    if request.user != message.user:
        return HttpResponse('You are not the owner of this message')

    if request.method == 'POST':
        form = MessageForm(request.POST, instance=message)
        if form.is_valid():
            form.save()
            return redirect('Room', pk=message.room.id) 
    return render(request, 'base/edit_message.html', {'form': form})


@login_required(login_url='login')
def delete_message(request, pk):
    message = get_object_or_404(Message, id=pk)  

    if request.user != message.user:
        return HttpResponse('You are not allowed to delete this message!')

    if request.method == 'POST':
        room_id = message.room.id 
        message.delete()
        return redirect('Room', pk=room_id)  

    return render(request, 'base/delete.html', {'obj': message})


@login_required(login_url='login')
def updateUser(request):
    user = request.user  #This retrieves the currently logged-in user.
    form = UserForm(instance=user)  #This initializes a Django ModelForm (UserForm) with the current user’s data.
    
    if request.method == 'POST':
        form = UserForm(request.POST,request.FILES,instance=user) #This updates the form with the new data submitted by the user.
        if form.is_valid():
            form.save()
            return redirect('user-profile',pk = user.id)


    return render(request,'base/update-user.html',{'form':form})


def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    return render(request,'base/topics.html',{'topics':topics})

def activitiesPage(request):
    room_messages = Message.object.all()
    return render(request,'base/activity.html',{'room_messages',room_messages})








'''
request.GET.get('q'):
Retrieves the search query from the URL.
If no query is provided, it defaults to an empty string.

Room.objects.filter(topic__name__contains=q):
Filters rooms based on whether the topic’s name contains the search query.

'''


#for messages=room.message_set.all()
'''
room – This is an instance of the Room model.

message_set – This is Django’s default related name for a reverse relationship when using a ForeignKey. 

.all() – Retrieves all related objects from the database.
'''