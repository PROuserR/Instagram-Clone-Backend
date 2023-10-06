from django.contrib.auth.models import User
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from .serializers import *
from .models import *


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def list_users(request):
    users = User.objects.exclude(id=request.user.id)
    users_serializer = UserSerializer(users, many=True)

    final_data = []
    for user in users_serializer.data:
        try:
            profile = Profile.objects.get(user=user['id'])
            final_data.append(
                {'id': user['id'], 'username': user['username'], 'profile_picture': str(profile.image)})
        except:
            pass
    return Response(final_data)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def list_followed_users(request, my_id):
    profile = Profile.objects.get(user=my_id)
    following = profile.following
    following_ids = []
    for following in following.values():
        following_ids.append(following['id'])

    final_data = []

    for following_id in following_ids:
        profile = Profile.objects.get(user=following_id)
        user = User.objects.get(id=following_id)
        final_data.append({'id': user.id, 'username': user.username, 'profile_picture': str(
            profile.image), 'last_seen': user.last_login})

    return Response(final_data)


@api_view(['POST', 'GET'])
@authentication_classes([TokenAuthentication])
def update_profile(request, user_id):
    try:
        profile = Profile.objects.get(user=user_id)
        serializer = ProfileSerializer(instance=profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
    except:
        serializer = ProfileSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
def follow_user(request, my_id, user_id):
    following_user = Profile.objects.get(user=User.objects.get(id=my_id))
    followed_user = Profile.objects.get(user=User.objects.get(id=user_id))

    following = following_user.following
    following.add(user_id)

    followers = followed_user.followers
    followers.add(my_id)

    followed_user.save()
    followed_user.save()

    return Response('Successfully completed!')


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
def unfollow_user(request, my_id, user_id):
    following_user = Profile.objects.get(user=User.objects.get(id=my_id))
    followed_user = Profile.objects.get(user=User.objects.get(id=user_id))

    following = following_user.following
    following.remove(user_id)

    followers = followed_user.followers
    followers.remove(my_id)

    followed_user.save()
    followed_user.save()

    return Response('Successfully completed!')


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
def create_profile(request):
    serializer = ProfileSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
    else:
        return Response(serializer.errors)

    return Response(serializer.data)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def get_my_user_info(request):
    user = request.user
    print('Userrr getinfo', user)
    profile = Profile.objects.get(user=user.id)
    return Response({'my_id': user.id, 'my_username': user.username, 'my_profile_picture': str(profile.image)})


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def get_profile(request, user_id):
    if user_id == 0:
        user_id = request.user.id
    profile = Profile.objects.get(user=user_id)
    profile_serializer = ProfileSerializer(profile)

    user = User.objects.get(id=user_id)
    user_serializer = UserSerializer(user)

    posts = Post.objects.filter(owner=user_id)
    post_serializer = PostSerializer(posts, many=True)

    final_data = {}
    for key in profile_serializer.data.keys():
        final_data[key] = profile_serializer.data[key]

    for key in user_serializer.data.keys():
        final_data[key] = user_serializer.data[key]

    posts = []
    for post in post_serializer.data:
        posts.append(dict(post))

    final_data['posts'] = posts

    return Response(final_data)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def get_comments(request, post_id):
    post = Post.objects.get(id=post_id)
    post_comments = post.comments
    serializer = CommentSerializer(post_comments, many=True)
    comments = []
    final_data = []
    for comment in serializer.data:
        comments.append(comment)
        profile = Profile.objects.get(user=comment['commenter'])
        profile_serializer = ProfileSerializer(profile)

        user = User.objects.get(id=comment['commenter'])
        user_serializer = UserSerializer(user)

        data = {}
        data['username'] = user_serializer.data['username']
        data['user_id'] = user_serializer.data['id']
        data['image'] = profile_serializer.data['image']
        data['comment'] = comment

        final_data.append(data)

    return Response(final_data)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def get_post(request, post_id):
    post = Post.objects.get(id=post_id)
    profile = Profile.objects.get(user=post.owner)
    serializer = PostSerializer(post)
    photoes_urls = []
    for photo_id in serializer.data['photoes']:
        photoes_urls.append(str(Photo.objects.get(id=photo_id)))

    final_data = dict(serializer.data)
    final_data['photoes'] = photoes_urls
    final_data['image'] = str(profile.image)
    final_data['username'] = profile.user.username
    final_data['profile_id'] = profile.id
    return Response(final_data)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
def save_post(request, my_id, post_id):
    post = Post.objects.get(id=post_id)
    post.saved = True
    post.saving_user_id = my_id
    post.save()
    return Response('Post saved!')


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
def unsave_post(request, my_id, post_id):
    post = Post.objects.get(id=post_id)
    post.saved = False
    post.saving_user_id = my_id
    post.save()
    return Response('Post unsaved!')


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def get_saved_posts(request, user_id):
    posts = Post.objects.filter(saved=True, saving_user_id=user_id)
    serializer = PostSerializer(posts, many=True)

    final_data = []
    for post in serializer.data:
        data = {}
        for key in post.keys():
            data[key] = post[key]
            user = User.objects.get(id=post['owner'])
            profile = Profile.objects.get(user=user)
            data['username'] = user.username
            data['image'] = str(profile.image)
            data['profile_id'] = profile.id
            photoes_urls = []
            for photo_id in post['photoes']:
                photoes_urls.append(str(Photo.objects.get(id=photo_id)))
            data['photoes'] = photoes_urls
            if len(post['likes']) > 0:
                data['liker'] = Like.objects.get(
                    id=post["likes"][0]).liker.username
                data['liker_id'] = Like.objects.get(
                    id=post["likes"][0]).liker.id
        final_data.append(data)

    return Response(final_data)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def list_user_posts(request, user_id):
    if user_id == 0:
        user_id = request.user.id
    user = User.objects.get(id=user_id)
    posts = Post.objects.filter(owner=user).order_by('-date_added')
    serializer = PostSerializer(posts, many=True)

    final_data = []
    for post in serializer.data:
        final_data.append(dict(post))

    for chunk in final_data:
        chunk['photoes'] = str(Photo.objects.get(id=chunk['photoes'][0]))

    return Response(final_data)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def discover_posts(request):
    posts = Post.objects.all()
    random_posts = []
    if len(posts) < 10:
        for i in range(len(posts)):
            random_posts.append(posts[i])
    else:
        for i in range(10):
            random_posts.append(posts[i])

    serializer = PostSerializer(random_posts, many=True)

    final_data = []
    for post in serializer.data:
        final_data.append(dict(post))

    for chunk in final_data:
        chunk['photoes'] = str(Photo.objects.get(id=chunk['photoes'][0]))

    return Response(final_data)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def news_feed(request):
    profile = Profile.objects.get(user=request.user.id)
    following = profile.following
    following_ids = []
    for following in following.values():
        following_ids.append(following['id'])

    final_posts = []
    posts = Post.objects.all().order_by('-date_added')
    for post in posts:
        if post.owner.id in following_ids:
            final_posts.append(post)
    serializer = PostSerializer(final_posts, many=True)

    final_data = []
    for post in serializer.data:
        data = {}
        for key in post.keys():
            data[key] = post[key]
            user = User.objects.get(id=post['owner'])
            profile = Profile.objects.get(user=user)
            data['username'] = user.username
            data['image'] = str(profile.image)
            data['profile_id'] = profile.id
            photoes_urls = []
            for photo_id in post['photoes']:
                photoes_urls.append(str(Photo.objects.get(id=photo_id)))
            data['photoes'] = photoes_urls
            if len(post['likes']) > 0:
                data['liker'] = Like.objects.get(
                    id=post["likes"][0]).liker.username
                data['liker_id'] = Like.objects.get(
                    id=post["likes"][0]).liker.id
        final_data.append(data)
    return Response(final_data)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
def create_post(request):
    files = request.FILES.getlist('images')
    data = request.POST
    post = Post.objects.create(
        caption=data['caption'], owner=User.objects.get(id=request.user.id))

    for file in files:
        photo_serializer = PhotoSerializer(data={'photo': file})
        if photo_serializer.is_valid():
            photo_serializer.save()
            post.save()
            post.photoes.add(photo_serializer.data['id'])
            post.save()
        else:
            return Response(photo_serializer.errors)

    return Response('Post upload successfuly')


@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
def update_post(request, id):
    post = Post.objects.get(id=id)

    if request.method == 'GET':
        serializer = PostSerializer(instance=post)
    else:
        serializer = PostSerializer(instance=post, data=request.data)

        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.errors)

    return Response(serializer.data)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
def delete_post(request, id):
    post = Post.objects.get(id=id)
    post.delete()

    return Response('Post deleted!')


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
def add_comment(request, post_id):
    serializer = CommentSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        post = Post.objects.get(id=post_id)
        post.comments.add(serializer.data['id'])
        post.save()
        return Response(serializer.data)
    else:
        return Response(serializer.errors)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def get_likers(request, post_id):
    post = Post.objects.get(id=post_id)
    likes = post.likes
    serializer = LikeSerializer(likes, many=True)
    likers = []
    if len(serializer.data) > 0:
        for like in serializer.data:
            likers.append(User.objects.get(id=like['liker']).username)
    return Response(likers)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
def add_like(request, post_id):
    serializer = LikeSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        post = Post.objects.get(id=post_id)
        post.save()
        post.likes.add(serializer.data['id'])
        post.save()
        return Response(serializer.data)
    else:
        return Response(serializer.errors)


@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
def delete_like(request):
    like = Like.objects.last()
    like.delete()
    return Response('Like deleted!')


@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
def delete_comment(request, id):
    comment = Comment.objects.get(id=id)
    comment.delete()
    return Response('Comment deleted!')


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def get_activites(request):
    activites = Activity.objects.filter(
        influnced=request.user.id).order_by('date_added')
    serializer = ActivitySerializer(activites, many=True)
    final_data = []
    for activity in serializer.data:
        data = dict(activity)
        data['profile_image'] = str(
            Profile.objects.get(user=activity['influncer']).image)
        data['username'] = User.objects.get(id=activity['influncer']).username
        final_data.append(data)

    return Response(final_data)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
def add_activity(request):
    serializer = ActivitySerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

        return Response(serializer.data)
    else:
        print(serializer.errors)
        return Response(serializer.errors)


@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
def delete_activity(request):
    activity = Activity.objects.last()
    activity.delete()
    return Response('Activity deleted!')


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
def add_story(request):
    files = request.FILES.getlist('images')
    story = Story.objects.create(owner=request.user)
    for file in files:
        photo_serializer = PhotoSerializer(data={'photo': file})
        if photo_serializer.is_valid():
            photo_serializer.save()
            story.save()
            story.photoes.add(photo_serializer.data['id'])
            story.save()
        else:
            return Response(photo_serializer.errors)

    return Response('Story upload successfuly')


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def get_users_stories(request):
    profile = Profile.objects.get(user=request.user.id)
    following = [user['id'] for user in profile.following.values()]
    def order_by_date_added(
        data): return data.date_added.strftime('%Y-%m-%d-%H-%M-%S')
    stories = [Story.objects.get(owner=id)
               for id in following if Story.objects.filter(owner=id)]
    stories.sort(reverse=True, key=order_by_date_added)

    final_data = []
    for story in stories:
        profile_picture = str(Profile.objects.get(user=story.owner).image)

        final_data.append({'id': story.owner.id, 'username': story.owner.username, 'profilePicture': profile_picture,
                           'storyPhotoes': [str(Photo.objects.get(id=photo_id)) for photo_id in StorySerializer(story).data['photoes']],
                           'dateAdded': story.date_added})
    return Response(final_data)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def get_my_story(request):
    try:
        story = Story.objects.get(owner=request.user.id)
        story_serializer = StorySerializer(story)
        profile = Profile.objects.get(user=request.user.id)
        profile_serializer = ProfileSerializer(profile)
        story_photoes = []
        for story_photo_id in story_serializer.data['photoes']:
            story_photoes.append(str(Photo.objects.get(id=story_photo_id)))

        return Response({'storyPhotoes': story_photoes, 'profileImage': profile_serializer.data['image'],
                         'dateAdded': story_serializer.data['date_added'], 'username': User.objects.get(id=request.user.id).username})

    except:
        return Response([])


@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
def delete_story(request, id):
    story = Story.objects.get(owner=id)
    story.delete()
    return Response('Story deleted!')
