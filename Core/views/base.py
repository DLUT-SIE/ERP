from django.views import generic
from django.contrib.auth import views, mixins


# AUTH VIEWS
LoginView = views.LoginView
LogoutView = views.LogoutView

# GENERIC BASE
View = generic.View
RedirectView = generic.RedirectView
TemplateView = generic.TemplateView

# GENERIC DETAIL
DetailView = generic.DetailView

# GENERIC EDIT
CreateView = generic.CreateView
DeleteView = generic.DeleteView
UpdateView = generic.UpdateView
FormView = generic.FormView

# GENERIC LIST
ListView = generic.ListView

# Mixins
LoginRequiredMixin = mixins.LoginRequiredMixin
