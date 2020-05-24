from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect
from django.shortcuts import render,get_object_or_404

from .forms import CommentForm
from .models import Comments

def comment_thread(request,id):
    obj = get_object_or_404(Comments,id=id)

    initial_data = {
        'content_type':obj.content_type,
        'object_id':obj.object_id
    }
    form = CommentForm(request.POST or None, initial=initial_data)
    print(dir(form))
    print(form.errors)
    if form.is_valid():
        c_type = form.cleaned_data.get('content_type')
        content_type = ContentType.objects.get_for_model(obj.__class__)
        # content_type = ContentType.objects.get(model=c_type)
        obj_id = form.cleaned_data.get('object_id')
        content_data = form.cleaned_data.get('content')
        parent_obj = None
        try:
            parent_id = int(request.POST.get('parent_id'))
        except:
            parent_id = None

        if parent_id:
            parent_qs = Comments.objects.filter(id = parent_id)
            if parent_qs.exists() and parent_qs.count() == 1:
                parent_obj = parent_qs.first()

        # print(form.cleaned_data)
        new_comment, created = Comments.objects.get_or_create(
            user = request.user,
            content_type = content_type,
            object_id = obj_id,
            content = content_data,
            parent = parent_obj
        )
        return HttpResponseRedirect(new_comment.content_object.get_absolute_url())
    context = {
        'comment':obj,
        'form':form
    }
    return render(request,'blog_app/comment_thread.html', context)
