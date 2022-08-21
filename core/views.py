from django.shortcuts import render,redirect
from .models import Topic,Choice
from django.contrib import messages
from .forms import SignUpForm,AddPollForm,PrivacyForm,PasswordChangingForm
from django.contrib.auth import login,authenticate,logout,update_session_auth_hash
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
			if choice.name != request.POST['name']:
				choice.name = request.POST['name']
				choice.save()
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
					messages.success(request,'Account is created successfully!')
					login(request,authenticate(username=request.POST['username'],password=request.POST['password1']))
					return redirect('topics')

		else:
			form = SignUpForm()

		return render(request,'signup.html',{
		'form':form
		})

@login_required
def delete_account(request):
	if request.method == 'POST':
		password = request.POST['password']
		if request.user == authenticate(request,username=request.user.username,password=password):
			user = request.user
			logout(request)
			user.delete()
			messages.success(request,'User is deleted successfully!')
			return redirect('topics')
		else:
			messages.error(request,"Incorrect username or password")
			return redirect('delete-account')

	else:
		return render(request,'delete_account.html',{})

@login_required
def privacy_settings(request):
    form = PrivacyForm(request.POST or None,instance=request.user)

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("topics")

    return render(request,"privacy_settings.html",{"form":form})


@login_required
def change_password(request):
	if request.method == "POST":
		form = PasswordChangingForm(request.user,request.POST)
		if form.is_valid():
			user = form.save()
			update_session_auth_hash(request,user)
			messages.success(request,'Your password is changed successfully!')
			return redirect('topics')

	else:
		form = PasswordChangingForm(request.user)

	return render(request,'change_password.html',{'form':form})

def login_user(request):
	if request.user.is_authenticated:
		messages.error(request,'You are already logged in!')
		return redirect('topics')
	else:
		if request.method == 'POST':
			email = request.POST['email']
			password = request.POST['password']
			try:
				user = authenticate(request,username=User.objects.get(email=email),password=password)
			except:
				messages.error(request,'Incorrect username or password!')
				return redirect('login')
			if user is not None:
				login(request,user)
				messages.success(request,'Logged in successfully!')
				return redirect('topics')
			else:
				messages.error(request,'Incorrect username or password!')
				return redirect('login')

		return render(request,'login.html',{})