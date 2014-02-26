import json, os
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.conf import settings
from geonode.documents.models import Document
from django.contrib.contenttypes.models import ContentType
from geonode.documents.views import document_set_permissions
from django.core.urlresolvers import reverse
from models import WFPDocument, Category
from forms import DocumentForm

ALLOWED_DOC_TYPES = settings.ALLOWED_DOCUMENT_TYPES

def browse(request, template='wfpdocs/list.html'):
    from geonode.search.views import search_page
    post = request.POST.copy()
    post.update({'type': 'document'})
    request.POST = post
    return search_page(request, template=template)
    
@login_required
def upload(request):
    if request.method == 'GET':
        orientation_choices = WFPDocument.ORIENTATION_CHOICES
        format_choices = WFPDocument.FORMAT_CHOICES
        categories = Category.objects.all()
        
        form = DocumentForm()
        
        return render_to_response(
            'wfpdocs/upload.html',
            { 'form': form,
              'orientation_choices': orientation_choices,
              'format_choices': format_choices, 
              'categories': categories },
            RequestContext(request)
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

        # map document
        form = DocumentForm(request.POST)
        if form.is_valid():
            source = form.cleaned_data.get('source')
            publication_date = form.cleaned_data.get('publication_date')
            orientation = form.cleaned_data.get('orientation')
            format = form.cleaned_data.get('format')
            categories = form.cleaned_data.get('categories')
            regions = form.cleaned_data.get('regions')
            
        document = Document(content_type=content_type, object_id=object_id, 
            title=title, doc_file=doc_file, date=publication_date)
        document.owner = request.user
        document.save()
        document.regions = regions
        permissionsStr = request.POST['permissions']
        permissions = json.loads(permissionsStr)
        document_set_permissions(document, permissions)
        
        wfpdoc = WFPDocument(source = source, orientation=orientation,
            format=format, document=document)
        wfpdoc.save()
        wfpdoc.categories = categories
        return HttpResponseRedirect(reverse('document_metadata', args=(document.id,)))
