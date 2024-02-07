from django.shortcuts import render,HttpResponse
from .models import Post,BlogComment
# Create your views here.
from django.contrib import messages
from django.shortcuts import redirect
from blog.templatetags import extras

def blogHome(request):
    allposts=Post.objects.all()
    #print(allposts)
    context={'allposts':allposts}
    return render(request,'blog/blogHome.html',context)
    
    # return HttpResponse('This is blogHome. We keep all blog posted.')

def  blogPost(request,slug):
    #post=Post.objects.filter(slug=slug)
    post=Post.objects.filter(slug=slug).first()
    #print(post)
    comments=BlogComment.objects.filter(post=post,parent=None)
    replies=BlogComment.objects.filter(post=post).exclude(parent=None)
    replyDict={}
    for reply in replies:
        if reply.parent.sno not in replyDict.keys():
            replyDict[reply.parent.sno]=[reply]
        else:
            replyDict[reply.parent.sno].append(reply)
    print(comments)
    # print(replies)
    print(replyDict)
    
    context={'post':post,'comments':comments,'user':request.user,'replyDict':replyDict}
    return render(request,'blog/blogPost.html',context)
    
    # return HttpResponse(f'This is blogpost: {slug}')

def postComment(request):
    
    if request.method=="POST":
       comment=request.POST.get("comment")
       user=request.user
       postSno=request.POST.get("postSno")
       post=Post.objects.get(sno=postSno)
       parentSno=request.POST.get("parentSno")
       
       if parentSno == "":
        comments=BlogComment(comment=comment,user=user,post=post)
        comments.save()
        messages.success(request,"Your comment has been posted successfully")
       else:
         parent=BlogComment.objects.get(sno=parentSno)
         comments=BlogComment(comment=comment,user=user,post=post,parent=parent)
         comments.save()
         messages.success(request,"Your reply has been posted successfully")
    else:
        return HttpResponse("error")
    return redirect(f"/blog/{post.slug}")

def createpost(request):
    
    if request.user.is_authenticated:
        
      if request.method=="POST":
        title=request.POST.get('title')
        content=request.POST.get('content')
        slug=request.POST.get('slug')
        author=request.POST.get('author')
        image=request.FILES.get('image')
        userimage=request.FILES.get('userimage')
        
        post=Post(title=title,content=content,slug=slug,author=author,image=image,userimage=userimage)
        post.save()
        messages.success(request,"Your post has been created")
    
    else:
        messages.error(request,"Login first !!!")
        
    return render(request,'blog/form.html')