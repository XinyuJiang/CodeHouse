from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.login, name='login'),  # 最后一个斜杠要有，不然url找不到
    path('register/', views.register, name='register'),  # 最后一个斜杠要有，不然url找不到
    path('index/', views.index, name='index'),
    path('tech_index/', views.tech_index, name='tech_index'),
    path('<int:pk>/', views.Tiezi_DetailView.as_view(), name='tiezi_details'),
    path('chat_index/', views.chat_index, name='chat_index'),
    path('Java/', views.JavaView.as_view(), name='Java'),
    path('C/', views.CView.as_view(), name='C'),
    path('Csharp/', views.CsharpView.as_view(), name='C#'),
    path('C++/', views.CplusView.as_view(), name='C++'),
    path('Python/', views.PythonView.as_view(), name='Python'),
    path('R/', views.RView.as_view(), name='R'),
    path('person_index/', views.person_index, name='person_index'),
    path('Other/', views.other, name='Other'),
    path('postedit/', views.postedit, name='postedit'),
    path('tucao/', views.tucao, name='tucao'),
    path('kg/', views.kg, name='kg'),

]
