from django.db import models
from uuid import uuid4
from random import shuffle
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import timedelta

#Base Class

class BaseModel(models.Model):
    uid = models.UUIDField(primary_key=True,default=uuid4,editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
    
class Category(BaseModel):
    name = models.CharField(max_length=100)
    description  = models.TextField(default='')
    total_marks=models.IntegerField(default=0)
    total_questions=models.IntegerField(default=0)
    image = models.ImageField(upload_to='media/',default=None,null=True,blank=True)
    total_time = models.IntegerField(default=60)
    def __str__(self) -> str:
        return self.name
    
    def get_total(self):
        questions= Question.objects.filter(category=self)
        self.total_marks= sum(question.mark for question in questions)
        self.total_questions = len(questions)


    
    
class Question(BaseModel):
    category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name='questions')
    question = models.TextField()
    mark = models.IntegerField(default=5)
    
    def __str__(self) -> str:
        return f'Qut-{self.question} Cat-{self.category} Mark-{self.mark}'
    
    def get_answer(self):
        answers = list(Answer.objects.filter(question=self))
        shuffle(answers)
        return [
            {'answer':answer.answer,'is_correct':answer.is_correct} for answer in answers
        ]
    
    class Meta:
        ordering = ['uid']


class Answer(BaseModel):
    question = models.ForeignKey(Question,on_delete=models.CASCADE,related_name='answers')
    answer= models.TextField()
    is_correct = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f'{self.question} Ans-{self.answer} is correct-{self.is_correct}'
    
    class Meta:
        ordering = ['uid']
        

class GivenQuizQuestions(BaseModel):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer,on_delete=models.CASCADE)
    time_taken = models.IntegerField(default=0)
    points = models.IntegerField(default=0) 
    def __str__(self) -> str:
        return self.question.question
    
class Quiz(BaseModel):
    status_choice = (
        ('no','no'),
        ('yes','yes'),
        ('incomplete','incomplete'),
        
    )
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name='quiz',default=None)
    given_question = models.ManyToManyField(GivenQuizQuestions,blank=True)
    marks = models.IntegerField(default=0)
    total_marks=models.IntegerField(default=0)
    status = models.CharField(max_length=10,blank=True,default='no',null=True)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(blank=True,null=True)
    
    def calculateMarks(self):     
        marks = 0
        for i in self.given_question.all():
            if i.answer.is_correct:
                marks += i.question.mark
        self.marks = marks

    # def save(self,*args,**kwargs):
    #     print(self.start_time)
       
        # super(Quiz,self).save(*args,**kwargs)
    def __str__(self):
        return f'{self.user.username} {str(self.total_marks)}'
    
@receiver(post_save,sender=Quiz)
def update_marks(sender,instance,created,**kwargs):
    instance.end_time = instance.start_time + timedelta(minutes=instance.category.total_time)
    instance.calculateMarks()

    