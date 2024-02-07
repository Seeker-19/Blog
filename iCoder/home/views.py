from django.shortcuts import render,HttpResponse
from home.models import Contact
from blog.models import Post
# Create your views here.
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout

from django.shortcuts import redirect

#html pages
def home(request):
    return render(request,'home/home.html',{'user':request.user})
    # return HttpResponse('This is Home.')

def about(request):
    return render(request,'home/about.html')
    # return HttpResponse('This is about.')

def contact(request):
   # messages.error(request,'Welcome To Contact')
    if request.method=="POST":
        #print("we are using post request")
        name=request.POST.get('name')
        email=request.POST.get('email')
        phone=request.POST.get('phone')
        content=request.POST.get('content')
        #print(name,email,phone,content)
        if len(name)<2 or len(email)<3 or len(phone)<10 or len(content)<4:
            messages.error(request,"Pls fill the form correctly.")
        else:
            contact=Contact(name=name,email=email,phone=phone,content=content)
            contact.save()
            messages.success(request,"Your Message has been successfully sent.")
            
    return render(request,'home/contact.html')
    # return HttpResponse('This is contact.')
    
def search(request):
    
     query=request.GET.get('query')
     if len(query)>78:
        allposts=Post.objects.none()
     else:
        allpostsTitle=Post.objects.filter(title__icontains=query)
        allpostsContent=Post.objects.filter(content__icontains=query)
        allposts=allpostsTitle.union(allpostsContent)
         
     if allposts.count() == 0:
         messages.warning(request,"No Search Results found !!!")
     params={'allposts':allposts, 'query':query}
     return render(request,'home/search.html',params)
    #return HttpResponse('This is search')
    
    
#authenrication API's
def handleSignup(request):
     if request.method=="POST":
         #get post parameters
         username=request.POST.get('username')
         fname=request.POST['fname']
         lname=request.POST['lname']
         email=request.POST['email']
         password1=request.POST['password1']
         password2=request.POST['password2']
         
         #check for error inputs
         
         #username under 10 chars
         if len(username) < 2 or len(username) > 10 :
             messages.error(request,"Username must be under 10 characters and min 2")
             return redirect('home')
             
        #username must be alphabets and numbers
         if not username.isalpha():
             messages.error(request,"Username should only contain letters and numbers")
             return redirect('home')
          
        #passwords should match   
         if password1!=password2:
             messages.error(request,"Password do not match")
             return redirect('home')
         
         
         #create user
         myuser=User.objects.create_user(username,email,password1)
         myuser.first_name=fname
         myuser.last_name=lname
         myuser.save()
         messages.success(request,"Your iCoder account has been successfully created.")
         return redirect('/')
     else:
        return HttpResponse("404 -Not found")
    
def handleLogin(request):
    
    if request.method=="POST":
        #get post parameters
        loginusername=request.POST.get('loginusername')
        loginpassword=request.POST.get('loginpassword')
        
        user=authenticate(username=loginusername,password=loginpassword)
        
        #if password is wrong user become None
        
        if user is not None:
            login(request,user)
            messages.success(request,"Successfully Logged In ")
            return redirect('home')
        else:
            messages.error(request,"Invalid credentials, PLease try again")
            return redirect('home')
        
    else:
        return HttpResponse("404 -Not found")
            
     #return HttpResponse('login')
 
def handleLogout(request):
    
        logout(request)
        messages.success(request,"Successfully logged out")
        return redirect('home')
     #return HttpResponse('logout')
 
