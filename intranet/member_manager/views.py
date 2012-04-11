from django.shortcuts import render_to_response, HttpResponseRedirect
from django.http import HttpResponse
from django.template import RequestContext
from django.core.context_processors import csrf
from django.db.models import Q
from django.forms.util import ErrorList
from intranet.member_manager.models import Member
from intranet.member_manager.forms import NewMemberForm, EditMemberForm
import ldap

# Create your views here.
def main(request):
  return render_to_response('intranet/member_manager/main.html',{"section":"intranet","page":'members'})
  
def search(request):
  q = request.GET.get('q')
  if q:
    members = Member.objects.filter(Q(netid__icontains=q) | \
                                    Q(first_name__icontains=q) | \
                                    Q(last_name__icontains=q)) \
                            .order_by('last_name', 'first_name')
  else:
    members = Member.objects.order_by('last_name', 'first_name')
  
  return render_to_response('intranet/member_manager/search.html',{
    "section":"intranet",
    "page":'members',
    'members':members,
    'q':q})
  
def new(request):
  c = {}
  c.update(csrf(request))
  if request.method == 'POST': # If the form has been submitted...
      form = NewMemberForm(request.POST) # A form bound to the POST data
      if form.is_valid(): # All validation rules pass
          try:
            form.save()
            return HttpResponseRedirect('/') # Redirect after POST
          except ValueError:
            errors = form._errors.setdefault("username", ErrorList())
            errors.append(u"Not a valid netid")
          
  else:
      form = NewMemberForm() # An unbound form

  return render_to_response('intranet/member_manager/form.html',{
      'form': form,
      "section":"intranet",
      "page":'members',
      "page_title":"Create new Member"
    },context_instance=RequestContext(request))
    