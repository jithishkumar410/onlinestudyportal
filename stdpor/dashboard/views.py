from django.shortcuts import redirect,render
import os
from .forms  import *
from django.contrib import messages
from django.views import generic
from youtubesearchpython import VideosSearch
import requests
import wikipedia

import openai

 






# Create your views here.
def home(request):
    return render(request,'dashboard\home.html')
  

def notes(request):
    if request.method == "POST":
        form=NotesForm(request.POST)
        if form.is_valid():
            notes=Notes(user=request.user,title=request.POST['title'],des=request.POST['des'])
            notes.save()
        messages.success(request,f"Notes Added Succesfully")
    else:
        form = NotesForm()
    notes = Notes.objects.filter(user=request.user)
    context={'notes':notes,'form':form}
    return render(request,'dashboard/notes.html',context)

def dele(request,pk=None):
    Notes.objects.get(id=pk).delete()
    return redirect("notes")
    
class NotesView(generic.DetailView):
    model=Notes

def youtube(request):
    if request.method=='POST':
        form=DashboardForm(request.POST)
        text=request.POST['text']
        video= VideosSearch(text)
        result_list=[]
        for i in video.result()['result']:
            result_dict={
                "input":text,
                'title':i['title'],
                'duration':i['duration'],
                'thumbnail':i['thumbnails'][0]['url'],
                'channel':i['channel']['name'],
                'link':i['link'],
                'views':i['viewCount']['short'],
                'time':i['publishedTime']
            }
            desc =''
            if i['descriptionSnippet']:
                for j in i['descriptionSnippet']:
                    desc += j['text']
            result_dict['description']=desc
            result_list.append(result_dict)
            context={
                'form':form,
                     'results':result_list
                     }
        return render(request,"dashboard/youtube.html",context)

    else:
         form=DashboardForm()
    context={'form':form}
    return render(request,"dashboard/youtube.html",context)
   
def todo(request):
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            try:
                finished=request.POST["is_finished"]
                if  finished == 'on':
                    finished=True
                else:
                    finished=False
            except:
                finished = False
            todos = Todo(
                user = request.user,
                title=request.POST['title'],
                is_finished=finished

            )
            todos.save()

    else:
        form=TodoForm()
    todo = Todo.objects.filter(user=request.user)
    if len(todo) == 0:
        todos_done =True
    else:
       todos_done = False 
    context={
        'form':form,
        'todos':todo,
        'todos_done':todos_done

    }
    return render(request,"dashboard/todo.html",context)

def update(request,pk=None):
    todo = Todo.objects.get(id=pk)
    if todo.is_finished == True:
        todo.is_finished = False
    else:
        todo.is_finished == True
    todo.save()
    return redirect('todo')

def deleteT(request,pk=None):
    Todo.objects.get(id=pk).delete()
    return redirect("todo")

def books(request):
    if request.method=='POST':
        form=DashboardForm(request.POST)
        text=request.POST['text']
        url = "https://www.googleapis.com/books/v1/volumes?q="+text
        r=requests.get(url)
        answer = r.json()
        result_list=[]
        for i in range(10):
            result_dict={
                "input":text,
                'title': answer['items'][i]['volumeInfo']['title'],
                'subtitle': answer['items'][i]['volumeInfo'].get('subtitle'),
                'des': answer['items'][i]['volumeInfo'].get('description'),
                'count': answer['items'][i]['volumeInfo'].get('pageCount'),
                'categories': answer['items'][i]['volumeInfo'].get('categories'),
                'rate': answer['items'][i]['volumeInfo'].get('pageRating'),
                'thum': answer['items'][i]['volumeInfo'].get('imageLinks')['smallThumbnail'],
                'pre': answer['items'][i]['volumeInfo'].get('previewLink'),
               
               
            }
          
            result_list.append(result_dict)
            context={
                'form':form,
                'results':result_list
                     }
        return render(request,"dashboard/books.html",context)

    else:
        form=DashboardForm()
    context={'form':form}
    return render(request,'dashboard/books.html', context)

def diction(request):
    if request.method=='POST':
        form=DashboardForm(request.POST)
        text=request.POST['text']
        url = "https://api.dictionaryapi.dev/api/v2/entries/en_US/"+text
        r=requests.get(url)
        answer = r.json()
        print(answer)
       
        ph=answer[0]['phonetics'][0]['text']
        aud=answer[0]['phonetics'][0]['audio']
        defi=answer[0]['meanings'][0]['definitions'][0]['definition']
      
        syn=answer[0]['meanings'][0]['definitions'][0]['synonyms']
        context={
            'form':form,
            'i':text,
             'ph':ph,
             'aud':aud,
             'defi':defi,
             
             'syn':syn
        }
    
       
        
        return render(request,'dashboard/dictionary.html',context)
    else:
        form=DashboardForm()
        context={
        'form':form
         }
    return render(request,'dashboard/dictionary.html',context)

def wiki(request):
    if request.method=='POST':
        text=request.POST['text']
        form=DashboardForm(request.POST)
        s=wikipedia.page(text)
       
        context={
        'form':form,
        'title':s.title,
        'link':s.url,
        'details':s.summary


         
         }
        return render(request,'dashboard/wiki.html',context)
    else:
         form=DashboardForm(request.POST)
         context={
             'form':form
         }
    return render(request,'dashboard/wiki.html',context)


def register(request):
    if request.method=='POST':
        form = UserRegistration(request.POST)
        if form.is_valid():
            form.save()
            username=form.cleaned_data.get('username')
            return redirect("login")
    else:        
        form = UserRegistration()
    context={
        'form':form
    }
    return render(request,'dashboard/register.html',context)

def pro(request):
    todos=Todo.objects.filter(is_finished=False,user=request.user)
    if len(todos)==0:
        todos_done=True
    else:
        todos_done=False
    context={
       'todos':todos,
       'todos_done':todos_done
    }

    return render(request,'dashboard/profile.html',context)




def chatbot(request):
  
    
    if request.method == 'POST':
        openai.api_key = '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'
        message = request.POST.get('message')
      


        response = openai.Completion.create(
  model="text-davinci-003",
  prompt=message,
  temperature=0.5,
  max_tokens=256
 
)
        res=response['choices'][0]['text']
        
        context={
            'res':res
        }
    else:
         context={
            'res':''
        }
  
    return render(request, 'dashboard/chatbot.html',context)
    

def logout(request):
     return render(request,'dashboard/logout.html')
