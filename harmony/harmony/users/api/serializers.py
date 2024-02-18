from django.contrib.auth import get_user_model
from rest_framework import serializers
from harmony.users.models import User, Member, Community
from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import LoginSerializer, JWTSerializer


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the User model."""
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    date_joined = serializers.DateTimeField(read_only=True)
    type = serializers.ChoiceField(choices=User.UserType.choices, default=User.UserType.COMMUNITY)
    avatar = serializers.ImageField(required=False)
    is_superuser = serializers.BooleanField(read_only=True)
    is_staff = serializers.BooleanField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)

    class Meta:
        model = get_user_model()
        fields = [
            "id",
            "username",
            "email",
            "date_joined",
            "type",
            "avatar",
            "is_superuser",
            "is_staff",
            "is_active",
        ]

        extra_kwargs = {
            "url": {"view_name": "api:user-detail", "lookup_field": "pk"},
        }


class UserRegisterSerializer(RegisterSerializer):
    username = serializers.CharField(required=True, max_length=150)
    email = serializers.EmailField(required=True)
    password1 = serializers.CharField(required=True, write_only=True, style={"input_type": "password"})
    password2 = serializers.CharField(required=True, write_only=True, style={"input_type": "password"})
    type = serializers.ChoiceField(choices=User.UserType.choices, default=User.UserType.COMMUNITY)
    avatar = serializers.ImageField(required=False)

    class Meta:
        model = get_user_model()
        fields = [
            "username",
            "email",
            "password1",
            "password2",
            "type",
            "avatar",
        ]

    def validate(self, attrs):
        attrs = super().validate(attrs)
        attrs['username'] = attrs['username'].lower().strip()
        attrs['email'] = attrs['email'].lower().strip()

        if User.objects.filter(username=attrs['username']).exists():
            raise serializers.ValidationError("Username already exists.")
        if User.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError("Email already exists.")
        return attrs

    def save(self, request):
        user = super().save(request)
        user.username = self.validated_data.get('username')
        user.type = self.validated_data.get('type')
        user.avatar = self.validated_data.get('avatar')
        user.save()

        # create a member or community object based on the user type
        if user.type == User.UserType.MEMBER:
            Member.objects.create(user=user,
                                  prn_number="TEMP_PRN",
                                  date_of_birth="2000-01-01")
        elif user.type == User.UserType.COMMUNITY:
            Community.objects.create(user=user, name=f"{user.username}'s Community")

        return user


class UserLoginSerializer(LoginSerializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True, style={"input_type": "password"})
    email = None

    class Meta:
        model = get_user_model()
        fields = [
            "username",
            "password",
        ]


class UserLoginResponseSerializer(JWTSerializer):
    user = UserSerializer(read_only=True)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)

    class Meta:
        model = get_user_model()
        fields = [
            "user",
            "access",
            "refresh",
        ]
        extra_kwargs = {
            "user": {"read_only": True},
            "access": {"read_only": True},
            "refresh": {"read_only": True},
        }

    def validate(self, attrs):
        attrs = super().validate(attrs)
        attrs["user"] = UserSerializer(self.user).data
        return attrs



###################


class MemberSerializer(serializers.ModelSerializer):
    """Serializer for the Member model."""
    id = serializers.IntegerField(read_only=True)
    user = UserSerializer(read_only=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    prn_number = serializers.CharField(required=True)
    date_of_birth = serializers.DateField(required=True)

    class Meta:
        model = Member
        fields = [
            "id",
            "user",
            "first_name",
            "last_name",
            "prn_number",
            "date_of_birth",
        ]

        read_only_fields = ("id", "user", "prn_number")


class CommunitySerializer(serializers.ModelSerializer):
    """Serializer for the Community model."""
    id = serializers.IntegerField(read_only=True)
    user = UserSerializer(read_only=True)
    name = serializers.CharField(required=True)
    description = serializers.CharField(required=False)

    class Meta:
        model = Community
        fields = [
            "id",
            "user",
            "name",
            "description",
        ]

        read_only_fields = ("id", "user")
