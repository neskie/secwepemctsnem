from forms import *
from django.contrib.auth.decorators import login_required
@login_required
def edit_user(request):
    if request.method == "POST":
        uform = UserForm(data = request.POST)
        if uform.is_valid():
            user = uform.save()
    elif request.method == "POST":
        user = request.user
        uform = UserForm(first_name=user.first_name,last_name=user.last_name)
        c = RequestContext({
                'form': uform,
            })
