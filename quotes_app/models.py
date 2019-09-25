from django.db import models
import re 
import bcrypt

class UserManager(models.Manager):
    def registrationvalidator(self, postData):
        errors = {}
        userSameEmail = User.objects.filter(email = postData['email'])

        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['name']) <2:
            errors['name'] = "Name should be at least 2 characters"
        if len(postData['email']) <1:
            errors['email'] = "Email is required"
        if len(userSameEmail)>0:
            errors['emailTaken'] = "Email is already taken!"
        if not EMAIL_REGEX.match(postData['email']):    # test whether a field matches the pattern            
            errors['emailpattern'] = "Invalid email address!"
        if len(postData['password']) <1:
            errors['password']= "Password should be at least 8 characters"
        if postData['password'] != postData['confirmpassword']:
            errors['pwmatch']= "Passwords do not match"
        registereduser= User.objects.filter(email=postData['email'])
        print(registereduser)
        return errors

    def login_validator(self, postData):
        usersSameEmail= User.objects.filter(email= postData['email'])
        errors = {}
        if len(postData['email'])<1:
            errors['email']= "You must enter a email"
        if len(postData['password'])<1:
            errors['password']= "You must enter a password"
        if len(usersSameEmail)<1:
            errors['emailNOTFOUND']= "Email is not registered"
        else:
            user= usersSameEmail[0]
            if len(postData['password'])>0: 
                if bcrypt.checkpw(postData['password'].encode(), user.password.encode()):
                    print("password match")
                else:
                    print("failed password")
                    errors["passwordINVALID"]= "The password is incorrect"
       
        return errors   

class QuoteManager(models.Manager):
    def quote_validator(self, postData):
        errors= {}
        if len(postData['owner'])<2:
            errors['owner']= "Quoted by should be more than 2 character"
        if len(postData['message'])<10:
            errors['message']= "Message should be 10 or more characters"
        return errors

    
    



class User(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Quote(models.Model):
    message = models.CharField(max_length=255)
    quote_owner = models.CharField(max_length=255)
    poster = models.ForeignKey(User, related_name="poster_quotes", on_delete=models.CASCADE)
    favorites = models.ManyToManyField(User, related_name="favorites")
    objects = QuoteManager()
