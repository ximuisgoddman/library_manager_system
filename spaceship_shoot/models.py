from django.db import models
from users.models import MyUser


# Create your models here.
class SpaceshipShoot(models.Model):
    score = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now_add=True)
    game_leval = models.CharField(max_length=100)
    record_score = models.IntegerField()
    record_time = models.DateTimeField()
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    spaceship_shoot_user_id = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='spaceship_shoot')


def __str__(self):
    return self.user
