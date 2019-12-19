from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, CustomUserChangeForm, AboutForm, BookForm, SearchForm, SendMessageForm, QuestionForm, AnswerForm
from .models import AboutModel, BookModel, SendMessageModel, Question, Answer
import json
from django.http import HttpResponse
from django.db.models import Q
# Create your views here.
def GetResult(string):
    return BookModel.objects.filter(
        Q(tags1__icontains=string) | Q(tags2__icontains=string) | Q(tags3__icontains=string)
    )


def empty(request):
    return redirect('home')
    return render(request, 'CustomUser/empty.html')

def home(request):
    if request.method == "POST":
        fo = SearchForm(request.POST)
        if fo.is_valid():
            fo.save()
            print("valid")
            temp = GetResult(request.POST['searchq'])
            searchform = SearchForm
            if temp:
                return render(request, 'CustomUser/home.html', {"temp" : temp, "search" : searchform})
            else:
                return render(request, 'CustomUser/home.html', {"temp" : "not found", "search" : searchform})
        else:
            print("invalid")

    searchform = SearchForm
    alldata = BookModel.objects.all().order_by('-id')
    return render(request, 'CustomUser/home.html', {"search" : searchform, "alldata" : alldata[:5]})

def signup2(request):
    if request.method == "POST":
        enrollment = request.POST['enrollment']
        username = request.POST['username']
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            
            return redirect('home')
        else:
            return render(request, 'CustomUser/signup.html', {'form': form})

    else:
        form = CustomUserCreationForm
        return render(request, 'CustomUser/signup.html', {'form': form})
        
def about(request, usernameurl):
    f = AboutModel.objects.filter(username=usernameurl)
    if f:      
        return render(request, 'CustomUser/about.html', {"form" : f, "currentuser": request.user, "username" : f[0].username})
    else:
        return redirect('editabout')
        
def contact(request):
    def getneccessary():
        return SendMessageModel.objects.filter(
        Q(to__icontains=request.user) | Q(fromperson__icontains=request.user)
    )
    getall = getneccessary()
    return render(request, 'CustomUser/contact.html', {"data" : getall})

def AboutEdit(request):
    if request.method == "POST":
        PostForm = AboutForm(request.POST)
        if PostForm.is_valid():
            temp = AboutModel.objects.filter(username=request.user)
            if temp:
                temp = AboutModel.objects.get(username=request.user)
                temp.about = request.POST['about']
                temp.save()
            else:
                PostForm.save()
            return redirect('about', usernameurl=request.user)
        else:
            return render(request, 'CustomUSer/temp.html', {"form" : PostForm})
    else:
        form = AboutForm
        temp = AboutModel.objects.filter(username=request.user)
        if temp:
            temp = AboutModel.objects.get(username=request.user)
            ab = temp.about
        else:
            return render(request, 'CustomUser/AboutEdit.html', {"username" : request.user, "form" : form})
        
    return render(request, 'CustomUser/AboutEdit.html', {"username" : request.user, "form" : form, "ab" : ab})

def donate(request):
    if request.method == "POST":
        submitted = BookForm(request.POST, request.FILES)
        if submitted.is_valid():
            temp = submitted.save()
            return redirect('displaydonate', donatepage=temp.pk)
        else:
            form = BookForm
            print("not valid donaes")
            return render(request, "CustomUser/temp.html", {"form": submitted})

    form = BookForm
    
    return render(request, 'CustomUser/donate.html', {"form" : form})

def displaydonate(request, donatepage):
    requested_object = BookModel.objects.get(pk=donatepage)
    similar = GetResult(requested_object.tags1)
    similar = similar | (GetResult(requested_object.tags2))
    similar = similar | GetResult(requested_object.tags3)
    return render(request, 'CustomUser/displaydonate.html', {"displayinfo" : requested_object, "similar" : similar})

def sendmessage(request, postid, to, fromperson):
    if request.method == "POST":
        messageform = SendMessageForm(request.POST)
        if messageform.is_valid():
            messageobject = SendMessageModel(to=to, fromperson=fromperson, frompost=postid, mainmessage=messageform.cleaned_data['mainmessage'])
            messageobject.save()
            return redirect('contact')
    form = SendMessageForm
    return render(request, 'CustomUser/SendMessage.html', {"form" : form})

def ask(request):
    if request.method == "POST":
        submitted = QuestionForm(request.POST)
        ques = request.POST["question"]
        q = Question(question=ques, user=request.user)
        q.save()
        return redirect('home')
    form = QuestionForm
    return render(request, 'CustomUser/discuss.html',{"form" : form})

def topics(request):
    questions = Question.objects.all()
    return render(request, 'CustomUser/topics.html', {"questions": questions})

def topic_specific(request, id):
    if request.method == "POST":
        object = Question.objects.get(pk=id)
        submitted = AnswerForm(request.POST)
        desc = request.POST["answer"]
        saved = Answer(question=object,answer=desc,upvotes=0, user=request.user)
        saved.save()
        temp = object.answer_set.all()
        return redirect("topic_specific", id=id)
    object = Question.objects.get(pk=id)
    temp = object.answer_set.all()
    form = AnswerForm
    return render(request, 'CustomUser/topic_specific.html', {"object":object, "form":form, "temp":temp})