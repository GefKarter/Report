from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import User

class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    rating_author = models.SmallIntegerField(default=0)

    def update_rating(self):
        post_rating = self.post_set.aggregate(postRating = Sum("rating"))
        pRat = 0
        pRat += post_rating.get("postRating")

        comment_rating = self.authorUser.comment_set.aggregate(commentRating = Sum("rating"))
        cRat = 0
        cRat += comment_rating.get("commentRating")

        self.rating_author = pRat * 3 + cRat
        self.save()

class Category(models.Model):
    name_category = models.CharField(max_length=32, unique= True)


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete = models.CASCADE)
    news = "NW"
    article = "AC"
    category_choices = (
        (news, "Новость"),
        (article, "Статья")
    )
    category_type = models.CharField(max_length=2, choices = category_choices, default = article)
    date_creation = models.DateTimeField(auto_now_add = True)
    post_category = models.ManyToManyField(Category, through= "PostCategory")
    title = models.CharField(max_length= 128)
    text = models.TextField()
    rating = models.SmallIntegerField(default=0)

    def like(self):
        self.rating+=1
        self.save()

    def dislike(self):
        self.rating-=1
        self.save()


    def preview(self):
        return self.text[0:123] + "..."


class PostCategory(models.Model):
    post_through = models.ForeignKey(Post, on_delete=models.CASCADE)
    category_through = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    comment_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()


