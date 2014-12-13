from django.db import models

class Board(models.Model):
    name = models.CharField(max_length=30)

    def __unicode__(self):
        return self.name

class List(models.Model):
    name = models.CharField(max_length=30)
    board = models.ForeignKey(Board)

    def __unicode__(self):
        return self.name

class Card(models.Model):
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=100)
    due_date = models.DateField()
    list = models.ForeignKey(List)

    def __unicode__(self):
        return self.title

class Label(models.Model):
    name = models.CharField(max_length = 30)
    card = models.ForeignKey(Card)

    def __unicode__(self):
        return self.name

class Member(models.Model):
    name = models.CharField(max_length = 70)
    card = models.ManyToManyField(Card)

    def __unicode__(self):
        return self.name
