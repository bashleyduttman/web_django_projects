from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.core.mail import send_mail
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Posts,Comment_db,Custom_User,CustomUserManager,Follow,Chat_Room,Chat_Room_Message
from django.conf import settings
from django.db import models
from django.db.models import Q;


# Create your views here.
def main(request):
    blogss = Posts.objects.all()
    comments=Comment_db.objects.all()
    recent=Posts.objects.all().order_by('-create')[:10]
    # Queryset with specific field
    user=None
    try:
        user = Follow.objects.filter(follower=request.user).values_list('following', flat=True)
    except:
        user=[]

    # Convert to list


    user=list(user)


    return render(request, 'main.html', {'blogss': blogss,'comments':comments,'user':user,'recent':recent},)


def login_user(request):
    if (request.method == 'POST'):
        name = request.POST.get('username')
        password = request.POST.get('password')
        try:
            Custom_User.objects.get(name=name)
        except:
            return HttpResponse("user not found")
        user = authenticate(request, name=name, password=password)
        if user:
            login(request, user)
            return redirect('main')
        else:
            return HttpResponse("Invalid credentials")

    return render(request, 'login.html')


def logout_user(request):
    logout(request)
    return redirect("main")


def post_user(request):
    if (request.method == 'POST'):
        title = request.POST.get('title')
        content = request.POST.get('message')
        post = Posts(title=title, content=content, user=request.user, name=request.user)
        user=get_object_or_404(Custom_User,id=request.user.id)
        user.post+=1
        user.save()
        post.save()
        return redirect('main')

    return render(request, "post-user.html")


def delete_post(request, postId):
    Posts.objects.get(id=postId).delete()
    user=get_object_or_404(Custom_User,id=request.user.id)
    user.post=max(user.post-1,0)
    user.save()
    return redirect('main')


email = None


def send_email_to_user(email):
    message = "this is working well"
    subject = "change password"
    host = settings.EMAIL_HOST_USER
    email = email
    send_mail(subject, message, host, [email])


def change_password(request):
    if (request.method == 'POST'):
        email = request.POST.get('email')
        send_email_to_user(email)
        return redirect("new_password")
    return render(request, 'change_password.html')


def new_fpassword(request):
    if (request.method == 'POST'):
        password = request.POST.get("password")
        user = User.objects.filter(email='717822f111@kce.ac.in').first()
        print(f"Password after hashing: {user.password}")
        if user:

            user.set_password(password)

            user.save()
        else:
            print("no user exits")

    return render(request, "reset_password.html")
def comments(request,postId):
    if(request.method=='POST'):
        comment=request.POST.get('comment')
        comme=Comment_db(comment=comment,post_id=postId,name=request.user,user=request.user)

        comme.save()
    return redirect('main')

def profiles(request,profId):
    users=Custom_User.objects.get(id=profId)
    user=None
    try:
        user=Follow.objects.filter(follower=request.user).values_list('following',flat=True)
        user=list(user)
    except:
        user=[]


    return render(request,'profile.html',{"users":users,"user":user})



def followers_increase(request, user_id):
    user_to_follow = get_object_or_404(Custom_User, id=user_id)
    user=get_object_or_404(Custom_User,id=request.user.id)
    if request.user != user_to_follow:
        # Find if a follow relationship already exists
        follow = Follow.objects.filter(follower=request.user, following=user_to_follow).first()

        if follow:
            # If the follow relationship exists, remove it (unfollow)
            follow.delete()
            # Update the follower count
            user_to_follow.followers =max(user_to_follow.followers-1,0)

        else:
            # If the follow relationship does not exist, create it (follow)
            Follow.objects.create(follower=request.user, following=user_to_follow)
            # Update the follower count

            user_to_follow.followers += 1
            user.followings+=1


        # Save the updated user information
        user_to_follow.save()
        user.save()

    return redirect('main')
def signup(request):
    if(request.method=='POST'):
        name=request.POST.get("first_name")
        password=request.POST.get("password1")
        email=request.POST.get("email")
        image = request.FILES.get("profile_image")
        user = Custom_User.objects.create_user(name=name, email=email, password=password,image=image)

        login(request, user)
        return redirect("main")

    return render(request,'signup.html')
def search_post(request):
    query=request.GET.get('q')
    posts=None
    if query:
        posts=Posts.objects.filter(Q(title__icontains=query))

    return render(request,'main.html',{'blogss':posts})
def start_or_create_chat(request,otheruser):
    user_2=get_object_or_404(Custom_User,id=otheruser)
    if(request.user==user_2):
        return HttpResponse("cannot chat with yourself")
    room,created=Chat_Room.objects.get_or_create(user1=request.user if request.user.id<user_2.id else user_2,
                                      user2=user_2 if request.user.id<user_2.id else request.user)
    return redirect('chat_room_message',room_id=room.id)
def chat_room(request,room_id):
    room=get_object_or_404(Chat_Room,id=room_id)
    if(request.user!=room.user1 and request.user!=room.user2):
        return HttpResponse("cant access here")
    messages=Chat_Room_Message.objects.filter(room=room)
    if request.method=='POST':
        message=request.POST.get('message')
        Chat_Room_Message.objects.create(room=room,sender=request.user,context=message)
    return render(request,'chat-room.html',{'messages':messages})
def chat_room_list(request):
    lists=Chat_Room.objects.filter(user1=request.user)  | Chat_Room.objects.filter(user2=request.user)
    return render(request,'chat_room_list.html', {'rooms':lists})
