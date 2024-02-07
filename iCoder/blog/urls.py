from django. urls import path
from . import views
urlpatterns = [
     
    
    path('',views.blogHome,name='name'),
    path('postComment/',views.postComment,name='postComment'),
    path('form/',views.createpost,name='form'),
    path('<str:slug>/',views.blogPost,name='blog'),
    
    
    
]
