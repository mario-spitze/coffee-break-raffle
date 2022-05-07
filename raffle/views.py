from ast import Try
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

def change(request):

    raffleID = int(request.GET.get('raffleID'))
    compareID = int(request.GET.get('compare'))
    comparePerson = Person.objects.get(pk=compareID)
    changewithID = int(request.GET.get('changewith'))
    changewithPerson = Person.objects.get(pk=changewithID)

    pairingA = Pairing.objects.filter(Q(personA=compareID) | Q(personB=compareID)).filter(event=raffleID)[0]
    pairingB = Pairing.objects.filter(Q(personA=changewithID) | Q(personB=changewithID)).filter(event=raffleID)[0]

    if pairingA.personA == compareID:
        pairingA.personA = changewithPerson
    else:
        pairingA.personB = changewithPerson

    if pairingB.personA == changewithID:
        pairingB.personA = comparePerson
    else:
        pairingB.personB = comparePerson

    pairingA.save()
    pairingB.save()

    return HttpResponseRedirect('/raffle/listRaffle/' + str(raffleID))

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


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        pkID = self.kwargs['id'] 
        context['pkID'] = pkID

        showSum = self.request.GET.get('showSum')
        if showSum == '1':
            context['showSum'] = '1'

        comparePerson = None
        try:
            compareID = int(self.request.GET.get('compare'))
            if compareID >= 0:
                comparePerson = Person.objects.get(pk=compareID)
        except:
            None

        if comparePerson != None:
            context['comparePerson'] = comparePerson
            object_list = context['object_list']
            for entry in object_list:
                entry.personA.repeate = Pairing.objects.all().filter(personA=entry.personA, personB=compareID).count()
                entry.personA.repeate += Pairing.objects.all().filter(personA=compareID, personB=entry.personA).count()
                entry.personB.repeate = Pairing.objects.all().filter(personA=entry.personB, personB=compareID).count()
                entry.personB.repeate += Pairing.objects.all().filter(personA=compareID, personB=entry.personB).count()
           
            context['object_list'] = object_list

        return context
        

    def get_queryset(self): # new
        object_list = []
        pk_url_kwarg = "post_id"
        query = self.kwargs['id']  

#        all_queryset = QuerySet.create(list(chain(Site.objects.all(), Medium.objects.all())))
        object_list.extend(list(Pairing.objects.filter(
                Q(event=query)
        )))

        for entry in object_list:

            entry.personA.cleanings = Pairing.objects.all().filter(cleaning_task=True).filter(Q(personA=entry.personA)|Q(personB=entry.personA)).count()
            entry.personB.cleanings = Pairing.objects.all().filter(cleaning_task=True).filter(Q(personA=entry.personB)|Q(personB=entry.personB)).count()

            entry.repeate = Pairing.objects.all().filter(personA=entry.personA, personB=entry.personB).count()
            entry.repeate += Pairing.objects.all().filter(personA=entry.personB, personB=entry.personA).count()
            entry.repeate -= 1

        return object_list