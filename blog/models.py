from django.db import models

# Create your models here.
class Article(models.Model):
  """Encapsulate the data of a blog Article by an author. """

  #blank = true means we can create a title even if we dont specify a value
  title = models.TextField(blank=True)
  author = models.TextField(blank=True)
  text= models.TextField(blank=True)
  #Whenever we create a blog Article, it was set this field to the current time
  published = models.DateTimeField(auto_now=True)
  image_file = models.ImageField(blank=True)

  

  def __str__(self):
    """return a string representation of this model instance"""
    return f"{self.title} by {self.author}"
  