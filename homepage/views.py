from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User,auth
from django.contrib.auth import login, authenticate
from django.contrib import messages
from .forms import SignupForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from quesa.settings import EMAIL_HOST_USER
from .models import Question, Genre, Like
import json

# Create your views here.
def home(request):
    return render(request, 'title.html')


def signup(request):
    form=SignupForm()
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            message = render_to_string('acc_active_email.html', {
                'user':user, 'domain':current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })

            mail_subject = 'Activate your quesa account.'
            from_email = EMAIL_HOST_USER
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message,from_email, to=[to_email])
            email.send()
            messages.info(request, 'Please Check your email.')
            return redirect('home')

    return render(request, 'registration.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        auth.login(request, user)
        messages.success(request, 'User Created Successfully.')
        return redirect('feed')
    else:
        return HttpResponse('Activation link is invalid!')


def login(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request,user)
            messages.success(request, 'User logged in Successfully.')
            return redirect('feed')
        else:
            messages.info(request,'Invalid credentials')
            return redirect('login')
    else:
        return render(request,'login.html')


@login_required(login_url='login')
def feed(request):
    question = Question.objects.all().order_by('-time')
    genre = Genre.objects.all().order_by('genre')
    return render(request,'homepagequesa.html',{'question':question, 'genre':genre})

def specific(request,category):
    question = Question.objects.filter(genre=category).order_by('-time')
    genre = Genre.objects.all().order_by('genre')
    return render(request, 'homepagequesa.html', {'question': question, 'genre':genre})

def answer(request):
        question = Question.objects.filter(status=False).order_by('-time')
        return render(request,'newquestions.html',{'question':question})

def answerpage(request, id):
    if request.method == 'GET':
        question = Question.objects.get(pk = id)
        genre = Genre.objects.all()
        return render(request,'newanswer.html',{'question':question, 'genre':genre})
    
    if request.method == 'POST':
        answer = request.POST['answer']
        anms = request.POST['anonymous']
        qid = int(request.POST.get("id"))
        question = Question.objects.get(id=qid)
        current_user = request.user
        question.status = True
        question.likecount = 0
        question.dislikecount = 0
        question.answer = answer
        if anms == "yes":
            anonymous = User.objects.get(username='anonymous')
            question.auser = anonymous
        else:
            question.auser = current_user
        question.save()
        messages.success(request, 'Answered Successfully.')
        return redirect('feed')

def ask(request):
    genre = Genre.objects.all().order_by('genre')
    return render(request,'newask.html',{'genre':genre})

def question(request):
    genreid = request.POST['genre']
    content = request.POST['question']
    anms = request.POST['anonymous']
    #genreid = form.cleaned_data.get('genre')
    #content = form.cleaned_data.get('question')
    current_user = request.user
    if anms == "yes":
        anonymous = User.objects.get(username='anonymous')
        q = Question(content= content, status= False, likecount = 0, dislikecount = 0, answer=" ", auser = current_user, genre_id= genreid,quser= anonymous)
    else:
        q = Question(content= content, status= False, likecount = 0, dislikecount = 0, answer=" ", auser = current_user, genre_id= genreid,quser= current_user)
    q.save()
    messages.success(request, 'Question added to the Database Successfully.')
    return redirect('feed')


def like(request):
    #if request.method == 'POST':
    user = request.user
    qid = request.GET['qid']
    question = Question.objects.get(id=qid)

    if Like.objects.filter(lname_id = user.id, ques_id=qid).exists():
        Like.objects.filter(lname_id = user.id, ques_id=qid).delete()
        question.likecount = question.likecount - 1
        question.time = question.time
        question.save()
        message = 'You unliked this'
    else:
        l = Like(like = True, lname_id = user.id, ques_id = qid)
        l.save()
        question.likecount = question.likecount + 1
        question.time = question.time
        question.save()
        message = 'You liked this'

    ctx = {'likes_count': question.likecount, 'message': message}
    return HttpResponse(json.dumps(ctx), content_type='application/json')


def logout(request):
    auth.logout(request)
    messages.success(request, 'User logged out successfully.')
    return redirect('/')