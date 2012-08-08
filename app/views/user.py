from django.http import HttpResponse, HttpResponseRedirect
from app.models import Op

__author__ = 'yousuf'

from django.template import loader, Context, RequestContext
from django.contrib.auth.models import User
from app.common.user import get_user
from app.forms.register import CompleteRegistrationForm
from app.forms.ops import OpForm, OpLinkForm, CommentForm


def home(request):
    user = get_user(request)
    template = loader.get_template('dahsboard/home.html')
    push_vars = Context({
        'user': user,
        })
    if not user.profile.is_enabled:
        form = CompleteRegistrationForm
        if request.method == 'POST':
            form = form(request.POST, instance=user.profile)
            form.save()
            user.profile.is_enabled = True
            user.profile.save()
        else:
            form = form(instance=user.profile)
        push_vars.update({
            'form': form,
        })
    else:
        oplinkform = OpLinkForm
        opform = OpForm
        commentform = CommentForm
        if request.method == 'POST':
            if request.POST.getlist('action')[0] == 'Comment':
                opid = request.POST['opid']
                op = Op.objects.get(id=opid)
                commentform = commentform(request.POST)
                comment = commentform.save(commit=False)
                comment.user = user
                comment.save()
                op.comments.add(comment)
                op.save()
                return HttpResponseRedirect('.')
            else:
                oplinkform = oplinkform(request.POST)
            #oplinkform.user_id = user
                oplink = oplinkform.save(commit=False)
                oplink.user = user
                oplink.save()
                opform = opform(request.POST)
                op = opform.save(commit=False)
                op.user = user
                op.save()
                op.links.add(oplink)
                opform.save()
                return HttpResponseRedirect('.')
        else:
            ops = Op.objects.filter(user = user).order_by('-added')
            push_vars.update({
                'ops': ops,
                'commentform': commentform,
            })
        push_vars.update({
            'oplinkform': oplinkform,
            'opform': opform
        })
    push_vars = RequestContext(request, push_vars)
    return HttpResponse(
        template.render(
            push_vars
        )
    )