from rest_framework import serializers
from .models import People, Address

class AddressSerializers(serializers.ModelSerializer):
	class Meta:
		model = Address
		fields = ['street', 'city', 'State', 'Zip_code',]




class peopleSerializers(serializers.ModelSerializer):
	address = AddressSerializers()
	class Meta:
		model = People 
		fields = ['Name','age', 'email', 'sex', 'height', 'weight', 'relationship', 'address',]
		# depth = 1

	def create(self, validated_data):
		address_data = validated_data.pop('address')
		address = Address.objects.create(**address_data)
		validated_data["address"] = address 
		people = People.objects.create(**validated_data)
		return people


	def update(self, instance, validated_data):
		address = validated_data.get('address')
		instance.address.street = address.get('street', instance.address.street)
		instance.address.city = address.get('city', instance.address.city)
		instance.address.State = address.get('State', instance.address.State)
		instance.address.Zip_code = address.get('Zip_code', instance.address.Zip_code)
		instance.address.save()
		instance.Name = validated_data.get("Name", instance.Name)
		instance.age = validated_data.get("age", instance.age)
		instance.email = validated_data.get("email", instance.email)
		instance.sex = validated_data.get("sex", instance.sex)
		instance.height = validated_data.get("height", instance.height)
		instance.weight = validated_data.get("weight", instance.weight)
		instance.relationship = validated_data.get("relationship", instance.relationship)
		instance.save()
		return instance