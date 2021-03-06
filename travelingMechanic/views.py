from django.shortcuts import render, redirect
from django.views.generic import CreateView, DetailView, DeleteView
from .models import Commission, webUser, review
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse
from .forms import createReview
from django import forms
import json
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import os

# Create your views here.
def home(request):
    context = {
        'commissions': Commission.objects.all(),
        'title': 'Home',
        'API_URL': os.environ.get('API_KEY_URL')
    }
    if request.method == "POST":
        pknum = request.POST.get('pknum')
        response_data = {}
        com = Commission.objects.filter(id=pknum).first()
        if(com.author != request.user.webuser):
            com.taker = request.user.webuser
            com.save()
            response_data['result'] = "Successfully Updated Commission!"
        else:
            response_data['result'] = "Failed!"
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        return render(request, 'travelingMechanic/home.html', context)

class CommissionDetailView(LoginRequiredMixin, DetailView):
    model = Commission
    template_name = 'travelingMechanic/detailed.html'


class CommissionCreateView(LoginRequiredMixin,CreateView):
    model = Commission
    template_name = 'travelingMechanic/commissions.html'
    fields = ['title', 'description', 'askPrice', 'lat', 'long', 'images']

    def form_valid(self, form):
        form.instance.author = webUser.objects.all().filter(user=self.request.user).first()
        return super().form_valid(form)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['lat'].widget = forms.HiddenInput()
        form.fields['long'].widget = forms.HiddenInput()
        form.fields['images'] = forms.ImageField()
        form.fields['images'].required = False
        return form

@login_required
def review(request):
    if request.method == 'POST':
        c_form = createReview(request.POST, request.FILES, initial={'author':request.user.webuser})
        if (c_form.is_valid()):
            print(c_form.cleaned_data)
            c_form.save()
            messages.success(request, 'Your review is posted!')
            return redirect('home')
    else:
        c_form = createReview(initial={'author':request.user.webuser})
    context = {'title':'Submit review', 'c_form':c_form}
    return render(request,'travelingMechanic/submitReview.html',context)

class CommissionDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Commission
    success_url = '/'

    def test_func(self):
        commission = self.get_object()
        if self.request.user == commission.author.user:
            return True
        return False

