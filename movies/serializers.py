from rest_framework import serializers
from .models import Collections
from django.contrib.auth.models import User
from collections import Counter
from django.http import JsonResponse
import requests

class MovieApiSerializer(serializers.ModelSerializer):
    def call_movie_api(self, domain, validated_data):
        user = "iNd3jDMYRKsN1pjQPMRz2nrq7N99q4Tsp9EY9cM0"
        pwd = "Ne5DoTQt7p8qrgkPdtenTK8zd6MorcCR5vXZIJNfJwvfafZfcOs4reyasVYddTyXCz9hcL5FGGIVxw3q02ibnBLhblivqQTp4BIC93LZHj4OppuHQUzwugcYu7TIC5H1"
        if 'page' in validated_data:
            page = validated_data['page']
        else:
            page = None
        if page is not None:
            url = "https://demo.credy.in/api/v1/maya/movies/" + "?page=" + page
        else:
            url = "https://demo.credy.in/api/v1/maya/movies/"
        response = requests.get(url, auth=(user, pwd))
        new_response = response.json()
        if 'is_success' not in new_response:
            if page is not None:
                new_response['next'] = domain.split("movies")[0] + "movies/?page=" + str(int(page) + 1)
                new_response['previous'] = domain.split("movies")[0] + "movies/?page=" + str(int(page) - 1)
            else:
                new_response['next'] = domain.split("movies")[0] + "movies/?page=2"
                new_response['previous'] = None
        return JsonResponse(new_response)

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(username=validated_data['username'], password=validated_data['password'])
        return user

class CollectionsPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collections
        fields = ('uuid', 'title', 'description', 'movies')

    def create(self, validated_data):
        title = validated_data['title']
        description = validated_data['description']
        movies = validated_data['movies']
        user = validated_data['user']
        collection = Collections.objects.create(title=title, description=description, movies=movies, user=user)
        return collection

class CollectionsGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collections
        fields = ('title', 'uuid', 'description')

    def count_genres(self, movies, count_genres):
        for movie in movies:
            genres = movie['genres'].split(",")
            for genre in genres:
                if genre:
                    if genre not in count_genres:
                        count_genres[genre] = 1
                    else:
                        count_genres[genre] = count_genres[genre] + 1
        return count_genres

    def get_collections(self, data):
        collections_list = []
        count_genres = {}
        favourite_genres = ""
        for collection in data:
            title = collection.title
            description = collection.description
            uuid = collection.uuid
            movies = collection.movies
            collections_list.append({"title": title, "uuid": uuid, "description": description})
            count_genres = self.count_genres(movies, count_genres)
        top_genres = Counter(count_genres).most_common(3)
        favourite_genres = str(top_genres[0][0] + ", " + top_genres[1][0] + ", " + top_genres[2][0])
        response = JsonResponse({"is_success": True, "data": {"collections": collections_list, "favourite_genres": favourite_genres}})
        return response

class SingleCollectionPutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collections
        fields = ('title', 'description', 'movies')

    def update(self, instance, validated_data):
        if 'title' in validated_data:
            instance.title = validated_data['title']
        if 'description' in validated_data:
            instance.description = validated_data['description']
        if 'movies' in validated_data:
            instance.movies = validated_data['movies']
        instance.save()
        return JsonResponse({"is_success": True})

class SingleCollectionGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collections
        fields = ('title', 'description', 'movies')

    def get_collection(self, instance):
        title = instance.title
        description = instance.description
        movies = instance.movies
        return JsonResponse({"title": title, "description": description, "movies": movies})
