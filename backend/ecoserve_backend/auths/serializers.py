from rest_framework import serializers
from users.models import User,Profile
from phonenumber_field.serializerfields import PhoneNumberField

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length = 8 , min_length = 5,style = {'input_type':'password'}
                                     ,required=True,write_only=True)
    confirm_password = serializers.CharField(max_length = 8 , min_length = 5,style = {'input_type':'password'}
                                             ,required=True,write_only=True)
    phone_number = serializers.CharField()
    email = serializers.EmailField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    other_name = serializers.CharField(required=False)


    class Meta:
        model = User
        fields = ['id','email','phone_number','first_name','last_name'
                  ,'other_name','password','confirm_password','date_joined']
    
    def validate(self,attrs):
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')
        email = attrs.get('email')

        if User.objects.filter(phone_number=attrs['phone_number']).exists():
            raise serializers.ValidationError({'phone number',('This number is registered for another user')})
        
        if User.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError({'Email',('This email is registered for another user')})

        if password != confirm_password:
            raise serializers.ValidationError("Passwords do not match.")
          
        return super().validate(attrs)
    
    def create(self,validated_data):

        confirm_password = validated_data.pop('confirm_password')
        return User.objects.create_user(**validated_data)

class UserLoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True,max_length = 16 , min_length = 5,style = {'input_type':'password'})
    phone_number = PhoneNumberField()
    # email = serializers.CharField(source='user.email',write_only=True)

    class Meta:
        model = User
        fields = ['id','phone_number','password']
    
    def validate(self,attrs):

        if User.objects.filter(phone_number=attrs['phone_number']).exists():
            raise serializers.ValidationError({'phone number',('This number is registered for another user')})
        
        return super().validate(attrs)
    
    def create(self,validated_data):

        return User.objects.create_user(**validated_data)