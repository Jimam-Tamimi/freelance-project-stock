from django.db import models
from django.contrib.auth.models import AbstractBaseUser, AnonymousUser, PermissionsMixin,BaseUserManager
import random
import string





# # class UserManager(BaseUserManager):
# #     """
# #     Django requires that custom users define their own Manager class. By
# #     inheriting from `BaseUserManager`, we get a lot of the same code used by
# #     Django to create a `User` for free.
# #     All we have to do is override the `create_user` function which we will use
# #     to create `User` objects.
# #     """

# #     def create_user(self, email, password=None, **extra_fields):
# #         """Create and return a `User` with an email and password."""

# #         if email is None:
# #             raise TypeError('Users must have an email address.')

# #         user = self.model(email=self.normalize_email(email), **extra_fields)
# #         user.set_password(password)
# #         user.save()

# #         return user
    

# #     def create_superuser(self, email, password):
# #         """
# #       Create and return a `User` with superuser powers.
# #       Superuser powers means that this use is an admin that can do anything
# #       they want.
# #       """
# #         if password is None:
# #             raise TypeError('Superusers must have a password.')

# #         user = self.create_user(email, password)
# #         user.is_superuser = True
# #         user.is_staff = True
# #         user.save()

# #         return user
    
    

# # class User(AbstractBaseUser, PermissionsMixin):
# #     # Each `User` needs a human-readable unique identifier that we can use to
# #     # represent the `User` in the UI. We want to index this column in the
# #     # database to improve lookup performance.
# #     # username = models.CharField(db_index=True, max_length=255, unique=True)

# #     # We also need a way to contact the user and a way for the user to identify
# #     # themselves when logging in. Since we need an email address for contacting
# #     # the user anyways, we will also use the email for logging in because it is
# #     # the most common form of login credential at the time of writing.
# #     email = models.EmailField(db_index=True, unique=True)

# #     # When a user no longer wishes to use our platform, they may try to delete
# #     # there account. That's a problem for us because the data we collect is
# #     # valuable to us and we don't want to delete it. To solve this problem, we
# #     # will simply offer users a way to deactivate their account instead of
# #     # letting them delete it. That way they won't show up on the site anymore,
# #     # but we can still analyze the data.
# #     is_active = models.BooleanField(default=True)

# #     # The `is_staff` flag is expected by Django to determine who can and cannot
# #     # log into the Django admin site. For most users, this flag will always be
# #     # falsed.
# #     is_staff = models.BooleanField(default=False)

# #     # More fields required by Django when specifying a custom user model.
# #     full_name = models.CharField(
# #         null=True,
# #         blank=True,
# #         max_length=256
# #     )

# #     # The `USERNAME_FIELD` property tells us which field we will use to log in.
# #     # In this case, we want that to be the email field.
# #     USERNAME_FIELD = 'email'
# #     REQUIRED_FIELDS = []

# #     # Tells Django that the UserManager class defined above should manage
# #     # objects of this type.
# #     objects = UserManager()

# #     def __str__(self):
# #         """
# #         Returns a string representation of this `User`.
# #         This string is used when a `User` is printed in the console.
# #         """
# #         return self.email

# #     def get_full_name(self):
# #         """
# #       This method is required by Django for things like handling emails.
# #       Typically, this would be the user's first and last name. Since we do
# #       not store the user's real name, we return their username instead.
# #       """
# #         return self.full_name





class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **other_fields):
        if not email:
            raise ValueError('You must provide email address')
        email = email.lower()
        user = self.model(email=email, **other_fields)
        user.set_password(password)
        user.save()
        Token.objects.create(user=user)
        return user
        
        

    def create_superuser(self, email, password, **other_fields):
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_staff', True)

        return self.create_user(email, password, **other_fields)



class MyUser(AbstractBaseUser, PermissionsMixin):
    id = models.BigAutoField(primary_key=True, blank=False, null=False)
    email = models.EmailField(max_length=90, blank=False, unique=True)
    username = models.CharField(max_length=90, default="u",  blank=True)
    timeStamp=models.DateTimeField(auto_now_add=True, blank=True)

    
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'

    

    def __str__(self):
        return self.username


class Token(models.Model):
    
    def get_random_alphanumeric_string():
        letters_and_digits = string.ascii_letters + string.digits
        result_str = ''.join((random.choice(letters_and_digits) for i in range(15)))
        return result_str
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, null=False, blank=False)
    token = models.CharField('Token', default=get_random_alphanumeric_string, max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user)

