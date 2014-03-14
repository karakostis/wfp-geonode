import json, os
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.conf import settings
from geonode.documents.models import Document
from django.contrib.contenttypes.models import ContentType
from geonode.documents.views import document_set_permissions
from django.core.urlresolvers import reverse
from models import WFPDocument, Category
from forms import DocumentForm
from geonode.maps.views import _perms_info
from geonode.documents.views import DOCUMENT_LEV_NAMES, IMGTYPES

ALLOWED_DOC_TYPES = settings.ALLOWED_DOCUMENT_TYPES

def document_browse(request, template='wfpdocs/document_list.html'):
    from geonode.search.views import search_page
    post = request.POST.copy()
    post.update({'type': 'document'})
    request.POST = post
    return search_page(request, template=template)

def document_detail(request, docid):
    """
    The view that show details of each document
    """
    document = get_object_or_404(Document, pk=docid)
    if not request.user.has_perm('documents.view_document', obj=document):
        return HttpResponse(loader.render_to_string('401.html',
            RequestContext(request, {'error_message':
                _("You are not allowed to view this document.")})), status=403)
    try:
        related = document.content_type.get_object_for_this_type(id=document.object_id)
    except:
        related = ''

    document.popular_count += 1
    document.save()

    return render_to_response("wfpdocs/document_detail.html", RequestContext(request, {
        'permissions_json': json.dumps(_perms_info(document, DOCUMENT_LEV_NAMES)),
        'document': document,
        'imgtypes': IMGTYPES,
        'related': related
    }))
    
@login_required
def document_upload(request):
    if request.method == 'GET':
        orientation_choices = WFPDocument.ORIENTATION_CHOICES
        format_choices = WFPDocument.FORMAT_CHOICES
        categories = Category.objects.all()
        
        form = DocumentForm()
        
        return render_to_response(
            'wfpdocs/document_upload.html',
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
            page_format = form.cleaned_data.get('page_format')
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
            page_format=page_format, document=document)
        wfpdoc.save()
        wfpdoc.categories = categories
        return HttpResponseRedirect(reverse('document_metadata', args=(document.id,)))
        
@login_required
def document_metadata(request, docid, template='documents/document_metadata.html'):
    document = Document.objects.get(id=docid)

    poc = document.poc
    metadata_author = document.metadata_author

    import ipdb;ipdb.set_trace()
    if request.method == "POST":
        document_form = DocumentForm(request.POST, instance=document, prefix="resource")
    else:
        document_form = DocumentForm(instance=document, prefix="resource")

    if request.method == "POST" and document_form.is_valid():
        new_poc = document_form.cleaned_data['poc']
        new_author = document_form.cleaned_data['metadata_author']
        new_keywords = document_form.cleaned_data['keywords']

        if new_poc is None:
            if poc.user is None:
                poc_form = ProfileForm(request.POST, prefix="poc", instance=poc)
            else:
                poc_form = ProfileForm(request.POST, prefix="poc")
            if poc_form.has_changed and poc_form.is_valid():
                new_poc = poc_form.save()

        if new_author is None:
            if metadata_author.user is None:
                author_form = ProfileForm(request.POST, prefix="author", 
                    instance=metadata_author)
            else:
                author_form = ProfileForm(request.POST, prefix="author")
            if author_form.has_changed and author_form.is_valid():
                new_author = author_form.save()

        if new_poc is not None and new_author is not None:
            the_document = document_form.save()
            the_document.poc = new_poc
            the_document.metadata_author = new_author
            the_document.keywords.add(*new_keywords)
            the_document.save()
            return HttpResponseRedirect(reverse('document_detail', args=(document.id,)))

    if poc.user is None:
        poc_form = ProfileForm(instance=poc, prefix="poc")
    else:
        document_form.fields['poc'].initial = poc.id
        poc_form = ProfileForm(prefix="poc")
        poc_form.hidden=True

    if metadata_author.user is None:
        author_form = ProfileForm(instance=metadata_author, prefix="author")
    else:
        document_form.fields['metadata_author'].initial = metadata_author.id
        author_form = ProfileForm(prefix="author")
        author_form.hidden=True

    return render_to_response(template, RequestContext(request, {
        "document": document,
        "document_form": document_form,
        "poc_form": poc_form,
        "author_form": author_form,
    }))
