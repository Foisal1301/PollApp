from django.db import models
from django.contrib.auth.models import User

class Topic(models.Model):
	name = models.CharField(blank=False,max_length=250)
	owner = models.ForeignKey(User,on_delete=models.CASCADE)

	def __str__(self):
		return f"{self.name} ( {self.owner} )"

	def total_voters(self):
		choices = Choice.objects.filter(topic__id=self.id)
		total_voters = 0
		for i in choices:
			total_voters += i.voters.count()

		return total_voters

class Choice(models.Model):
	name = models.CharField(blank=False,max_length=250)
	topic = models.ForeignKey(Topic,on_delete=models.CASCADE)
	voters = models.ManyToManyField(User,blank=True)

	def __str__(self):
		return f"{self.name}-{self.topic}-{self.voters.count()}"

	def percentage(self):
		total_voters = self.topic.total_voters()
		try:
			return self.voters.count() * 100 / total_voters
		except ZeroDivisionError:
			return 0