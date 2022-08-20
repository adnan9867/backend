from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken
from .constants import *
from .serializers import *


class UserSignupView(ModelViewSet):
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = UserSignupSerializer

    def create(self, request, *args, **kwargs):
        try:
            serializer = UserSignupSerializer(data=request.data, context={'request': request})
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({SUCCESS: True, STATUS_CODE: 200, MESSAGE: "You have successfully signup"},
                                status=status.HTTP_200_OK)
            return Response({SUCCESS: False, STATUS_CODE: 400, ERROR: serializer.errors}, )
        except Exception as e:
            return Response({SUCCESS: False, STATUS_CODE: 400, ERROR: str(e.args[0])},
                            status=status.HTTP_400_BAD_REQUEST)


class UserLoginViewSet(ModelViewSet):
    serializer_class = None
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        try:
            data = request.data
            user = User.objects.filter(email=data['email']).first()  # get user by email
            if not user:
                return Response({SUCCESS: False, STATUS_CODE: 400, ERROR: "User not found"},
                                status=status.HTTP_400_BAD_REQUEST)
            if not user.check_password(data['password']):  # check password
                return Response({SUCCESS: False, STATUS_CODE: 400, ERROR: "Password is incorrect"},
                                status=status.HTTP_400_BAD_REQUEST)
            refresh = RefreshToken.for_user(user)  # generate JWT token
            response = {
                'access_token': str(refresh.access_token),
                'refresh_token': str(refresh),
                'user': user.id,
            }
            return Response({SUCCESS: True, MESSAGE: "You have successfully login", DATA: response},
                            status=status.HTTP_200_OK)
        except Exception as e:
            return Response({SUCCESS: False, "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UserProfileViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer

    def list(self, request, *args, **kwargs):
        try:
            """ Get user profile by using token """
            serializer = UserProfileSerializer(request.user)
            return Response({SUCCESS: True, STATUS_CODE: 200, DATA: serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({SUCCESS: False, STATUS_CODE: 400, ERROR: str(e.args[0])},
                            status=status.HTTP_400_BAD_REQUEST)


class UserProfileListViewSet(ModelViewSet):
    permission_classes = [IsAdminUser]
    serializer_class = UserProfileSerializer

    def list(self, request, *args, **kwargs):
        """ Only Admin can list all users """
        try:
            user = User.objects.all()
            serializer = self.serializer_class(user, many=True)
            return Response({SUCCESS: True, STATUS_CODE: 200, DATA: serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({SUCCESS: False, STATUS_CODE: 400, ERROR: str(e.args[0])},
                            status=status.HTTP_400_BAD_REQUEST)


class PostViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def list(self, request, *args, **kwargs):
        """ Get all posts by login user"""
        try:
            posts = Post.objects.filter(author=request.user).order_by('-id')
            serializer = self.serializer_class(posts, many=True)
            return Response({SUCCESS: True, STATUS_CODE: 200, DATA: serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({SUCCESS: False, STATUS_CODE: 400, ERROR: str(e.args[0])},
                            status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        """ Create new post """
        try:
            data = request.data
            data['author'] = request.user.id
            serializer = self.serializer_class(data=data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({SUCCESS: True, STATUS_CODE: 200, MESSAGE: "Post created successfully"},
                                status=status.HTTP_200_OK)
            return Response({SUCCESS: False, STATUS_CODE: 400, ERROR: serializer.errors}, )
        except Exception as e:
            return Response({SUCCESS: False, STATUS_CODE: 400, ERROR: str(e.args[0])},
                            status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        """ Update post by id """
        try:
            data = request.data
            pk = data['id']
            post = Post.objects.filter(id=pk).first()
            if not post:
                return Response({SUCCESS: False, STATUS_CODE: 400, ERROR: "Post not found"},
                                status=status.HTTP_400_BAD_REQUEST)
            serializer = PostSerializer(post, data=data, partial=True, context={'request': request})
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({SUCCESS: True, STATUS_CODE: 200, MESSAGE: "Post updated successfully"},
                                status=status.HTTP_200_OK)
            return Response({SUCCESS: False, STATUS_CODE: 400, ERROR: serializer.errors}, )
        except Exception as e:
            return Response({SUCCESS: False, STATUS_CODE: 400, ERROR: str(e.args[0])},
                            status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        """ Delete post by id """
        try:
            pk = request.query_params.get('id')
            post = Post.objects.filter(id=pk).first()
            if not post:
                return Response({SUCCESS: False, STATUS_CODE: 400, ERROR: "Post not found"},
                                status=status.HTTP_400_BAD_REQUEST)
            if not post.author.id == request.user.id:
                return Response({SUCCESS: False, STATUS_CODE: 400, ERROR: "You are not author"},
                                status=status.HTTP_400_BAD_REQUEST)
            post.delete()
            return Response({SUCCESS: True, STATUS_CODE: 200, MESSAGE: "Post deleted successfully"},
                            status=status.HTTP_200_OK)
        except Exception as e:
            return Response({SUCCESS: False, STATUS_CODE: 400, ERROR: str(e.args[0])},
                            status=status.HTTP_400_BAD_REQUEST)


class PostListViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def list(self, request, *args, **kwargs):
        """ Get all posts """
        try:
            posts = Post.objects.all().order_by('-id')
            serializer = self.serializer_class(posts, many=True)
            return Response({SUCCESS: True, STATUS_CODE: 200, DATA: serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({SUCCESS: False, STATUS_CODE: 400, ERROR: str(e.args[0])},
                            status=status.HTTP_400_BAD_REQUEST)


class PostReactionViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = PostLikes.objects.all()
    serializer_class = PostReactionSerializer

    def post_like(self, request, *args, **kwargs):
        try:
            data = request.data
            data['user'] = request.user.id
            reaction = self.queryset.filter(user__id=request.user.id, post__id=data['post']).first()
            if reaction:
                reaction.delete()
                return Response({SUCCESS: True, STATUS_CODE: 200, MESSAGE: "Post unlike successfully"},
                                status=status.HTTP_200_OK)
            serializer = self.serializer_class(data=data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({SUCCESS: True, STATUS_CODE: 200, MESSAGE: "Post like successfully"},
                                status=status.HTTP_200_OK)
        except Exception as e:
            return Response({SUCCESS: False, STATUS_CODE: 400, ERROR: str(e.args[0])},
                            status=status.HTTP_400_BAD_REQUEST)
