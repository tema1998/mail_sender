from django.urls import path

from . import views

urlpatterns = [
    path("", views.Index.as_view(), name="index"),
    path("send-email", views.SendEmail.as_view(), name="send-email"),
    path("history", views.History.as_view(), name="history"),
    path("create-task", views.CreateTask.as_view(), name="create-task"),
    path("tasks", views.Tasks.as_view(), name="tasks"),
    path(
        "enable-disable-task",
        views.EnableDisableTask.as_view(),
        name="enable-disable-task",
    ),
    path("delete-task", views.DeleteTask.as_view(), name="delete-task"),
    path("signup", views.Signup.as_view(), name="signup"),
    path("signin", views.Signin.as_view(), name="signin"),
    path("logout", views.Logout.as_view(), name="logout"),
]
