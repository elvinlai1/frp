# Django create user

### 1、Set up Django data source
### PostgreSQL setting

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'myproject',
        'USER': 'myprojectuser',
        'PASSWORD': 'password1',  # actual password
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### 2、Sync data with database

```shell
python manage.py migrate         #
python manage.py makemigrations  #
```

### 3、Create user

**Using django shell to create normal user**

```shell
In [1]: from django.contrib.auth.models import User
In [2]: user=User.objects.create_user("manager1","manager1@frp.com","123456")
In [4]: user.set_password("123456")
In [6]: user.save()
```

### 4、Create superuser
### Superuser have access to all features
```shell
python manage.py createsuperuser --username=admin --email=admin@frp.com
```
### Superuser account info
### name: admin
### password: password1

### 5、Changing the password

**Using django shell to change password**

```shell
>>> from django.contrib.auth.models import User
>>> u = User.objects.get(username='manager1')
>>> u.set_password('654321')
>>> u.save()
```