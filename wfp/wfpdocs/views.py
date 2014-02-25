from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext

def browse(request, template='documents/document_list.html'):
    from geonode.search.views import search_page
    post = request.POST.copy()
    post.update({'type': 'document'})
    request.POST = post
    return search_page(request, template=template)
    
@login_required
def upload(request):
    if request.method == 'GET':
        return render_to_response('wfpdocs/upload.html',
                                  RequestContext(request),
                                  context_instance=RequestContext(request)
        )

    elif request.method == 'POST':
        
        try:
            content_type = ContentType.objects.get(name=request.POST['type'])
            object_id = request.POST['q']
        except:
            content_type = None
            object_id = None
        
        title = request.POST['title']
        doc_file = request.FILES['file']
        
        if len(request.POST['title'])==0:
            return HttpResponse(_('You need to provide a document title.'))
        if not os.path.splitext(doc_file.name)[1].lower()[1:] in ALLOWED_DOC_TYPES:
            return HttpResponse(_('This file type is not allowed.'))
        if not doc_file.size < settings.MAX_DOCUMENT_SIZE * 1024 * 1024:
            return HttpResponse(_('This file is too big.'))

        
        document = Document(content_type=content_type, object_id=object_id, title=title, doc_file=doc_file)
        document.owner = request.user
        document.save()
        permissionsStr = request.POST['permissions']
        permissions = json.loads(permissionsStr)
        document_set_permissions(document, permissions)

        return HttpResponseRedirect(reverse('document_metadata', args=(document.id,)))
