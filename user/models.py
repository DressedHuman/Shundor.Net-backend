from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField


class UserManager(BaseUserManager):
    """
    Custom manager for User model, handling user and superuser creation.
    """
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError("The Phone Number field must be set")

        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(phone_number, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model using phone number as the unique identifier.
    """
    phone_number = PhoneNumberField(unique=True, region="BD", blank=False, null=False)
    email = models.EmailField(unique=True, blank=True, null=True)

    is_verified = models.BooleanField(default=True)  # Phone/email verified
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ["email"]

    objects = UserManager()

    def __str__(self):
        return str(self.phone_number)


class UserProfile(models.Model):
    """
    Profile model for storing additional user information and preferences.
    """
    class UserType(models.TextChoices):
        CUSTOMER = "customer", "Customer"
        SUPPLIER = "supplier", "Supplier"
        RESELLER = "reseller", "Reseller"
        ADMIN = "admin", "Admin"

    class Gender(models.TextChoices):
        MALE = "M", "Male"
        FEMALE = "F", "Female"
        OTHER = "O", "Other"

    class RequestFor(models.TextChoices):
        SELLER = "seller", "seller"
        SUPPLIER = "supplier", "supplier"
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")

    user_type = models.CharField(max_length=20, choices=UserType.choices, default=UserType.CUSTOMER)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=1, choices=Gender.choices, blank=True, null=True)
    profile_image = models.ImageField(upload_to="profile_images/", blank=True, null=True)

    default_shipping_address = models.TextField(blank=True, null=True)
    default_billing_address = models.TextField(blank=True, null=True)



    is_request= models.BooleanField(blank=True, null=True)
    request_for = models.CharField(
        max_length=20,
        choices=RequestFor.choices,
        null=True,
        blank=True
    )

    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        Return a readable representation of the user profile.
        """
        return f"{self.first_name} {self.last_name}" if self.first_name and self.last_name else str(self.user)
    
    