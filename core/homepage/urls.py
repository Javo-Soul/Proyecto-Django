from views import *

urlpatterns =[
    #Supervisor
    path('homepage/index', IndexView.as_view(), name='index'),
]