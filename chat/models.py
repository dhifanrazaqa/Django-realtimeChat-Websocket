from django.db import models
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string

class Room(models.Model):
  roomName = models.CharField(max_length=200)
  slug = models.SlugField(unique=True)

  def __str__(self):
    return self.roomName

class Group(models.Model):
  participants = models.ManyToManyField(User)
  slug = models.SlugField(blank=True, null=True)

  def __str__(self):
    return self.slug
  
  def save(self, *args, **kwargs):
    """ Add Slug creating/checking to save method. """
    slug_save(self) # call slug_save, listed below
    super().save(*args, **kwargs)
# ...

def slug_save(obj):
  """ A function to generate a 5 character slug and see if it has been used and contains naughty words."""
  if not obj.slug: # if there isn't a slug
    obj.slug = get_random_string(8) # create one
    slug_is_wrong = True  
    while slug_is_wrong: # keep checking until we have a valid slug
        slug_is_wrong = False
        other_objs_with_slug = type(obj).objects.filter(slug=obj.slug)
        if len(other_objs_with_slug) > 0:
            # if any other objects have current slug
            slug_is_wrong = True
        if slug_is_wrong:
            # create another slug and check it again
            obj.slug = get_random_string(8)

class Message(models.Model):
  room = models.ForeignKey(Room, related_name='messages', on_delete=models.CASCADE, blank=True, null=True)
  group = models.ForeignKey(Group, related_name='messages', on_delete=models.CASCADE, blank=True, null=True)
  user = models.ForeignKey(User, related_name='messages', on_delete=models.CASCADE)
  content = models.TextField()
  createdAt = models.DateTimeField(auto_now_add=True)

  class Meta:
    ordering = ('createdAt',)
  def __str__(self):
    return f"{self.room} {self.user}"