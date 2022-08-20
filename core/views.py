from django.shortcuts import render,redirect
from .models import Topic,Choice
from django.contrib import messages
from .forms import SignUpForm,AddPollForm
from django.contrib.auth import login,authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

def topics(request):
	topics = Topic.objects.all()
	return render(request,'topics.html',{
			'topics':topics
		})

@login_required
def delete_topic(request,pk):
	target = Topic.objects.get(pk=pk)
	if request.user.is_superuser or request.user.id == target.owner.id:
		target.delete()
		messages.success(request,"Topic is deleted successfully")
	else:
		messages.error(request,"You are not allowed")
	return redirect('topics')

def topic(request,pk):
	topic = Topic.objects.get(pk=pk)
	choices = Choice.objects.filter(topic=topic)
	if request.method == "POST":
		for i in choices:
			if request.user in i.voters.all():
				i.voters.remove(request.user)

		try:
			selected_option = request.POST['choices']
			Choice.objects.get(pk=int(selected_option)).voters.add(request.user)
		except:
			pass

	return render(request,"topic.html",{
			'topic':topic,
			'choices':choices,
		})

@login_required
def update_topic(request,pk):
	topic = Topic.objects.get(pk=pk)
	if topic.owner == request.user or request.user.is_superuser:
		form = AddPollForm(request.POST or None, instance=topic)
		if request.method =="POST" and form.is_valid:
			form.save()
			messages.success(request,"Poll is updated successfully!")
			return redirect('topic',pk=topic.id)

		return render(request,'update_topic.html',{
			'form':form,
			'topic':topic
			})
	else:
		message.error(request,'You are not allowed')
		return redirect('topics')

@login_required
def add_topic(request):
	if request.method == "POST":
		form = AddPollForm(request.POST)
		if form.is_valid:
			topic = form.save(commit=False)
			topic.owner = request.user
			topic.save()
			return redirect('topic',pk=topic.id)
	else:
		form = AddPollForm()
		return render(request,'add_topic.html',{
				'form':form
			})

@login_required
def add_choice(request,pk):
	topic = Topic.objects.get(pk=pk)
	if request.user == topic.owner:
		if request.method == "POST":
			Choice.objects.create(name=request.POST['name'],topic=topic)
			return redirect('topic',pk=topic.id)

	else:
		messages.error(request,"You are not allowed!")
		return redirect('topic',pk=topic.id)

@login_required
def update_choice(request,pk):
	choice = Choice.objects.get(pk=pk)
	if request.user.is_superuser or request.user == choice.topic.owner:
		if request.method =="POST":
			choice.name = request.POST['name']
			messages.success(request,"choice is updated successfully!")
			return redirect('topic',pk=choice.topic.id)

		return render(request,'update_choice.html',{
			'choice':choice
			})
	else:
		message.error(request,'You are not allowed')
		return redirect('topic',pk=choice.topic.id)

@login_required
def delete_choice(request,pk):
	choice = Choice.objects.get(pk=pk)
	if request.user.is_superuser or request.user == choice.topic.owner:
		tp = choice.topic
		choice.delete()
		messages.success(request,"Option is deleted successfully!")
		return redirect('topic',pk=tp.id)
	else:
		messages.error(request,"You are not allowed!")
		return redirect('topic',pk=tp.id)
	

def signup(request):
	if request.user.is_authenticated:
		messages.error(request,'You are already logged in!')
		return redirect('topics')
	else:
		if request.method == "POST":
			form = SignUpForm(request.POST)
			email = request.POST['email']
			if User.objects.filter(email=email).exists():
				messages.error(request,"This email already exists!")
				return redirect('signup')
			else:
				if form.is_valid:
					form.save()
					login(request,authenticate(username=request.POST['username'],password=request.POST['password1']))
					return redirect('topics')

		else:
			form = SignUpForm()
			return render(request,'signup.html',{
				'form':form
				})