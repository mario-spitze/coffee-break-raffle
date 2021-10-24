from django.shortcuts import render
from django.http import HttpResponseRedirect
# Create your views here.
from .forms import CreatRaffleForm
from django.views import generic
from datetime import datetime
from django.db.models import Q
from django.db.models import Count

import random
from .models import *

def index(request):
    return HttpResponseRedirect('/raffle/createRaffle/')


def createRaffle(request):

    if request.method == 'POST':
        form = CreatRaffleForm(request.POST)
        if form.is_valid():
            random.seed(datetime.now())
            new_event = form.save()
            persons_set = form.cleaned_data.get('persons')
            persons_list = list(persons_set)
            random.shuffle(persons_list)
            print(persons_list)
            count = persons_set.count() - 1
            loops = count / 2
            while count >= 0:
                newPair = Pairing(id=None, event=new_event, personA=persons_list[count], personB=persons_list[count - 1])
                newPair.save()
                count = count - 2
            
            return HttpResponseRedirect('/raffle/listRaffle/' + str(new_event.id))

    else:
        form = CreatRaffleForm()
    return render(request, 'raffle/createRaffle.html', {'form': form})

class ListRaffleView(generic.ListView):
    template_name = 'raffle/listEntry.html'

    def get_queryset(self): # new
        object_list = []
        pk_url_kwarg = "post_id"
        query = self.kwargs['id']

#        all_queryset = QuerySet.create(list(chain(Site.objects.all(), Medium.objects.all())))
        object_list.extend(list(Pairing.objects.filter(
                Q(event=query)
        )))

        for entry in object_list:

            entry.repeate = Pairing.objects.all().filter(personA=entry.personA, personB=entry.personB).count()
            entry.repeate += Pairing.objects.all().filter(personA=entry.personB, personB=entry.personA).count()
            entry.repeate -= 1
            print(entry)

        return object_list