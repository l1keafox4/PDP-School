from rest_framework import serializers
from .models import Post, Category


class CategorySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField()

    def create(self, validated_data):
        category = Category.objects.create(**validated_data)
        return category

    def update(self, instance, validated_data):
        partial = validated_data.get('partial', False)
        if partial:
            instance.title = validated_data.get('title', instance.title)
        else:
            instance.title = validated_data.get('title', '')
        instance.save()
        return instance

class PostSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(required=False)
    slug = serializers.CharField(required=False)
    body = serializers.CharField(required=False)
    created = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        post = Post.objects.create(**validated_data)
        return post

    def update(self, instance, validated_data):
        partial = validated_data.get('partial', False)
        if partial:
            instance.name = validated_data.get('name', instance.name)
            instance.slug = validated_data.get('slug', instance.slug)
            instance.body = validated_data.get('body', instance.body)
        else:
            instance.name = validated_data.get('name', '')
            instance.slug = validated_data.get('slug', '')
            instance.body = validated_data.get('body', '')
        instance.save()
        return instance

