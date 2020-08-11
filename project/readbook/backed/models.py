from django.db import models
from account.models import *

# Create your models here.
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


# collection model
class Collection(models.Model):
    name = models.CharField(max_length=128)
    user = models.ForeignKey(Account,related_name='collections',on_delete=models.CASCADE)
    create_time=models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=('create_time',)

    def __str__(self):
        return '%d: %s' % (self.id,self.name)

# book model
class Book(models.Model):
    id = models.CharField(max_length=128, primary_key=True)
    title = models.CharField(max_length=128)
    authors = models.CharField(max_length=256)
    publisher = models.CharField(max_length=128)
    publish_date = models.CharField(max_length=128, null=True)
    page_count = models.IntegerField()
    avg_rating = models.DecimalField(max_digits=6,decimal_places=1,default=0,null=True)
    categories = models.CharField(max_length=128)
    ISBN = models.IntegerField(unique=True)
    imageLink = models.URLField(max_length = 256)
    description = models.TextField(null=True)
    added_times = models.PositiveIntegerField(null=True,default=0)
    collection = models.ManyToManyField(Collection,related_name='books',through='Collection_Book')

    def __str__(self):
      return '%s: %s' % (self.id,self.title)

# intermediate model
# to descrip the "add" action
class Collection_Book(models.Model):
    collection = models.ForeignKey(Collection,on_delete=models.CASCADE)
    book = models.ForeignKey(Book,on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now_add=True)
    # belongto :userId
    belongto = models.PositiveIntegerField()

    class Meta:
        unique_together=('collection','book')
        ordering=['create_time']
# set a goal
class Goal(models.Model):
    user = models.ForeignKey(Account,related_name='user_goal',on_delete=models.CASCADE)
    year = models.PositiveIntegerField(default=0)
    month = models.PositiveIntegerField(default=0)
    target = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together=('user','year','month')

# month record
class MonthRecord(models.Model):
    user = models.ForeignKey(Account,related_name='user_record',on_delete=models.CASCADE)
    year = models.PositiveIntegerField(default=0)
    month = models.PositiveIntegerField(default=0)
    total_nums = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together=('user','year','month')

class ReadedBook(models.Model):
    user = models.PositiveIntegerField()
    book_id=models.CharField(max_length=128)

    class Meta:
        unique_together=('user','book_id')

# 
class Review(models.Model):
    content = models.TextField(null=True)
    create_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(Account,related_name='review_user',on_delete=models.CASCADE)
    book = models.ForeignKey(Book,related_name='review_book',on_delete=models.CASCADE)
    like_count_num = models.PositiveIntegerField(default=0)

    # class Meta:
    #     unique_together=('user','book')


class LikeIt(models.Model):
    review = models.ForeignKey(Review,related_name='likeit_review',on_delete=models.CASCADE)
    user = models.ForeignKey(Account,related_name='likeit_user',on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    # need book id, bu i don't want foreignkey strick
    belongto_book = models.CharField(max_length=128)

    class Meta:
        unique_together=('user','review')

class Rating(models.Model):
    user = models.ForeignKey(Account,related_name='rating_user',on_delete=models.CASCADE)
    book = models.ForeignKey(Book,related_name='rating_book',on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(default=0)
    create_time=models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user','book')



# token_create_when_account_create
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

#goal_accomplish_add_when_book_added_to_collection


#goal_accomplish_less_when_book_delete_from_collection
