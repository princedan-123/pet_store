from rest_framework import serializers
from .models import User, Pet, Adoption, Client

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['is_staff', 'is_superuser', 'password']

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'

class PetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pet
        fields = '__all__'

class AdoptionSerializer(serializers.ModelSerializer):
    pet = PetSerializer(required=True)
    client = ClientSerializer(required=True)

    def validate_price(self, value):
        """Validates the price field to ensure it is greater than 0."""
        if value <= 0:
            raise serializers.ValidationError('Price must be above 0')
        return value
    
    def create(self, validated_data):
        """Overrides the default create method to accomodate nested writes."""
        pet = validated_data.pop('pet')
        client = validated_data.pop('client')
        pet, created_pet = Pet.objects.get_or_create(**pet)
        client, created_client = Client.objects.get_or_create(**client)
        adoption = Adoption.objects.create(pet=pet, client=client, **validated_data)
        return adoption
    class Meta:
        model = Adoption
        fields = '__all__'

