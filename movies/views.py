from django.http import JsonResponse
from rest_framework import generics
from rest_framework.permissions import AllowAny
from .serializers import RegisterSerializer, CollectionsPostSerializer, CollectionsGetSerializer
from .serializers import SingleCollectionPutSerializer, SingleCollectionGetSerializer, MovieApiSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Collections


class MovieApiResponse(generics.GenericAPIView):
    serializer_class = MovieApiSerializer

    def get(self, request):
        domain = request.build_absolute_uri()
        serializer = self.get_serializer()
        response = serializer.call_movie_api(domain, request.query_params)
        return response

class RegisterAPI(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh_token = TokenObtainPairSerializer.get_token(user=user)
        access_token = refresh_token.access_token
        return JsonResponse({
            "access_token": str(access_token),
            "refresh_token": str(refresh_token)
        })

class CollectionsView(generics.GenericAPIView):
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CollectionsPostSerializer
        elif self.request.method == 'GET':
            return CollectionsGetSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        collection = serializer.save(user=request.user)
        return JsonResponse({
            "collection_uuid": collection.uuid,
        })

    def get(self, request, *args, **kwargs):
        query_set = Collections.objects.filter(user=request.user)
        if query_set.exists():
            serializer = self.get_serializer()
            response = serializer.get_collections(query_set)
            return response
        else:
            return JsonResponse({"error": "collections are empty"}, status=404)

class SingleCollectionView(generics.GenericAPIView):
    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return SingleCollectionPutSerializer
        elif self.request.method == 'GET':
            return SingleCollectionGetSerializer

    def put(self, request, uuid, *args, **kwargs):
        query_set = Collections.objects.filter(uuid=uuid, user=request.user)
        if query_set.exists():
            instance = query_set[0]
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            response = serializer.save()
            return response
        else:
            return JsonResponse({"error": "uuid does not exist"}, status=404)

    def get(self, request, uuid):
        query_set = Collections.objects.filter(uuid=uuid, user=request.user)
        if query_set.exists():
            instance = query_set[0]
            serializer = self.get_serializer()
            response = serializer.get_collection(instance)
            return response
        else:
            return JsonResponse({"error": "uuid does not exist"}, status=404)

    def delete(self, request, uuid):
        query_set = Collections.objects.filter(uuid=uuid, user=request.user)
        if query_set.exists():
            instance = query_set[0]
            instance.delete()
            return JsonResponse({"is_success": True})
        else:
            return JsonResponse({"error": "uuid does not exist"}, status=404)
