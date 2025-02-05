from django.core.checks import messages
from django.shortcuts import redirect, render
from home.models import registration
# Create your views here.
from itertools import chain
from discover.models import interest,followers
from chatbox.models import chatrooms, usermessages
from complete.models import userdetails
from trending.views import get_hash_tags

def chatbox(request, room_code= 'asd123123'):
    if request.session['email']:
        email = request.session['email']
        user = registration.objects.filter(email=email)
        id = registration.objects.get(email=email)
        interests_all = interest.objects.all()
        interests = []
        for i in interests_all:
            interests.append(i)
        userid = id.pk
        other = None
        my_id = None
        counts = 0
        count_following = 0
        try:
            em = followers.objects.get(user_id=userid)
            other = [user_id for user_id in em.following.all()]
            count_following = len(other)
            my_id = [user_id for user_id in em.follow_me.all()]
            counts = len(my_id)


        except:
            pass
        user_data = userdetails.objects.all()
        mydetials = 0
        try:
            mydetials = userdetails.objects.get(owner_id=userid)
        except:
            pass
        other_user = registration.objects.all().exclude(email=email)
        trending_hashtags=get_hash_tags()
        dict1 = {
            'my_id': id,
            'email': email,
            'user': user,
            'others': other,
            'other': other_user,
            'followers': my_id,
            'count': counts,
            'count_following': count_following,
            'mydetials': mydetials,
            'userdata': user_data,
            'interests': interests,
            'trending_hashtags':trending_hashtags,
            'room_code': room_code
        }

        return render(request, 'chatglobal.html', dict1)

def room(request, room_code):
    if request.session['email']:
        email = request.session['email']
        rc = request.GET.get('query')
        user = registration.objects.filter(email=email)
        id = registration.objects.get(email=email)
        interests_all = interest.objects.all()
        interests = []
        for i in interests_all:
            interests.append(i)
        userid = id.pk
        other = None
        car = None
        my_id = None
        counts = 0
        count_following = 0
        vs_id = registration.objects.get(id=int(rc))
        vs_photo = userdetails.objects.get(owner_id=int(rc))
        opp_name = vs_id.first_name + ' ' + vs_id.last_name
        opp_photo = vs_photo.profile_pic
        # print(opp_photo)
        msg_for = None
        room_code = room_id_encoder(str(userid), rc)
        print(room_code)
        if chatrooms.objects.filter(userroomcode=room_code).exists():
            ii = chatrooms.objects.get(userroomcode = room_code)
            car = ii.id
            # print(car)
            msg_for = usermessages.objects.filter(roomcode = room_code).order_by('messagecreated')
        try:
            em = followers.objects.get(user_id=userid)
            other = [user_id for user_id in em.following.all()]
            count_following = len(other)
            my_id = [user_id for user_id in em.follow_me.all()]
            counts = len(my_id)


        except:
            pass
        user_data = userdetails.objects.all()
        mydetials = 0
        try:
            mydetials = userdetails.objects.get(owner_id=userid)
        except:
            pass
        other_user = registration.objects.all().exclude(email=email)
        trending_hashtags=get_hash_tags()
        dict1 = {
            'my_id': id,
            'email': email,
            'user': user,
            'others': other,
            'other': other_user,
            'followers': my_id,
            'count': counts,
            'count_following': count_following,
            'mydetials': mydetials,
            'userdata': user_data,
            'interests': interests,
            'trending_hashtags':trending_hashtags,
            'rie' : room_code,
            'stored_msg' : msg_for,
            'chat_id' : car,
            'opp_name' : opp_name,
            'opp_photo' : opp_photo,
        }
        return render(request, 'chatroom.html', dict1)
        
def room_id_encoder(user1, user2):
    room_name = [user1 , user2]
    room_code = user1 + user2
    f = chatrooms.objects.all()
    # print(f)
    for item in f:
        rav = item.commuserlist
        if user1 in rav:
            if user2 in rav:
                tav = chatrooms.objects.get(userroomcode = item.userroomcode)
                return tav.userroomcode
    
    room,created = chatrooms.objects.get_or_create(commuserlist= room_name, userroomcode = room_code)
    room.save()
    return room_code