from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=255)


class Test(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Question(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    question_text = models.TextField()
    sequence_number = models.IntegerField(default=0)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        # noinspection PyUnresolvedReferences
        return f'{self.test.title} - Question #{self.sequence_number}'


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_text = models.CharField(max_length=100)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        answer = self.answer_text[:10]
        # noinspection PyUnresolvedReferences
        return f'{self.question.test.title} - Question #{self.question.sequence_number} - {answer}...'


class UserProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)

    def __str__(self):

        return f'{self.user} - {self.question}'


class UserHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    success_percent = models.IntegerField(default=0)
