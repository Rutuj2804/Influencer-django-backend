from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class Skill(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Link(models.Model):
    title = models.CharField(max_length=500)
    link = models.TextField()

    def __str__(self):
        return self.title


class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, city, state, first_name, password=None):
        if not email:
            raise ValueError("Email field is required")
        if not username:
            raise ValueError("Username field is required")
        if not city:
            raise ValueError("City field is required")
        if not state:
            raise ValueError("State field is required")
        if not first_name:
            raise ValueError("First name field is required")
        user = self.model(
            email = self.normalize_email(email),
            username=username,
            city=city,
            state=state,
            first_name=first_name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, city, state,first_name,password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            city=city,
            state=state,
            first_name=first_name,
            password=password
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    email = models.EmailField(verbose_name="Email", max_length=500, unique=True)
    username = models.CharField(verbose_name="Username", max_length=30, unique=True)
    first_name = models.CharField(verbose_name="First name", max_length=255)
    last_name = models.CharField(verbose_name="Last name", max_length=255)

    instagram = models.CharField(max_length=500)
    facebook = models.CharField(max_length=500)
    youtube = models.CharField(max_length=500)
    isCompany = models.BooleanField(default=False, verbose_name="Is Company")
    skills = models.ManyToManyField(Skill)
    photo = models.ImageField(upload_to="display-pictures")
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=100)
    online = models.BooleanField(default=False)
    links = models.ManyToManyField(Link)
    description = models.TextField(verbose_name="Description")
    rate = models.IntegerField(default=0)
    raters_count = models.ManyToManyField("self")
    points = models.IntegerField(default=1)

    date_joined = models.DateTimeField(verbose_name="Date Joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="Last login", auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'city', 'state', 'first_name',]

    objects = MyAccountManager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True