import json, os, re

from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext, loader
from django.utils.translation import ugettext as _
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.core.exceptions import PermissionDenied
from django_downloadview.response import DownloadResponse
from django.views.decorators.cache import cache_page
from django.views.generic.edit import UpdateView, CreateView
from django.db.models import F

from geonode.documents.models import Document
from geonode.documents.forms import DocumentForm
from geonode.people.forms import ProfileForm
from geonode.security.views import _perms_info_json
from geonode.documents.models import IMGTYPES
from geonode.documents.views import _resolve_document
from geonode.documents.views import _PERMISSION_MSG_DELETE
from geonode.utils import build_social_links

from .models import WFPDocument, Category
from .forms import WFPDocumentForm

ALLOWED_DOC_TYPES = settings.ALLOWED_DOCUMENT_TYPES

_PERMISSION_MSG_DELETE = _("You are not permitted to delete this static map")
_PERMISSION_MSG_GENERIC = _('You do not have permissions for this static map.')
_PERMISSION_MSG_MODIFY = _("You are not permitted to modify this static map")
_PERMISSION_MSG_METADATA = _(
    "You are not permitted to modify this static map's metadata")
_PERMISSION_MSG_VIEW = _("You are not permitted to view this static map")


def _resolve_document(request, slug, permission='base.change_resourcebase',
                      msg=_PERMISSION_MSG_GENERIC, **kwargs):
    '''
    Resolve the document by the provided primary key and check the optional permission.
    '''
    #return resolve_object(request, Document, {'pk': docid},
    #                      permission=permission, permission_msg=msg, **kwargs)
    # TODO handle permissions here
    document = WFPDocument.objects.get(slug=slug)
    return document

def document_detail(request, slug):
    """
    The view that show details of each static map
    """
    document = None
    try:
        document = _resolve_document(
            request,
            slug,
            'base.view_resourcebase',
            _PERMISSION_MSG_VIEW)

    except Http404:
        return HttpResponse(
            loader.render_to_string(
                '404.html', RequestContext(
                    request, {
                        })), status=404)

    except PermissionDenied:
        return HttpResponse(
            loader.render_to_string(
                '401.html', RequestContext(
                    request, {
                        'error_message': _("You are not allowed to view this document.")})), status=403)

    if document is None:
        return HttpResponse(
            'An unknown error has occured.',
            mimetype="text/plain",
            status=401
        )

    else:
        #try:
        #    related = document.content_type.get_object_for_this_type(
        #        id=document.object_id)
        #except:
        #    related = ''
        # TODO figure out if we need this
        related = ''

        # Update count for popularity ranking,
        # but do not includes admins or resource owners
        if request.user != document.owner and not request.user.is_superuser:
            WFPDocument.objects.filter(id=document.id).update(popular_count=F('popular_count') + 1)

        metadata = document.link_set.metadata().filter(
            name__in=settings.DOWNLOAD_FORMATS_METADATA)

        # TODO handle permissions here
        #perms_json = _perms_info_json(document)
        perms_json = "{}"
        context_dict = {
            'permissions_json': perms_json,
            'resource': document,
            'metadata': metadata,
            'imgtypes': IMGTYPES,
            'related': related}

        if settings.SOCIAL_ORIGINS:
            context_dict["social_links"] = build_social_links(request, document)

        return render_to_response(
            "wfpdocs/document_detail.html",
            RequestContext(request, context_dict))


def wfpdocument_download(request, docid):
    document = get_object_or_404(WFPDocument, pk=docid)
    if not request.user.has_perm(
            'base.download_resourcebase',
            obj=document.get_self_resource()):
        return HttpResponse(
            loader.render_to_string(
                '401.html', RequestContext(
                    request, {
                        'error_message': _("You are not allowed to view this document.")})), status=401)
    return DownloadResponse(document.doc_file)


class DocumentUpdateView(UpdateView):
    #import ipdb;ipdb.set_trace()
    template_name = 'wfpdocs/document_form.html'
    pk_url_kwarg = 'docid'
    form_class = WFPDocumentForm
    queryset = WFPDocument.objects.all()
    context_object_name = 'wfpdocument'

    def form_valid(self, form):
        """
        If the form is valid, save the associated model.
        """
        import ipdb;ipdb.set_trace()
        self.object = form.save()
        return HttpResponseRedirect(
            reverse(
                'document_metadata',
                args=(
                    self.object.id,
                )))


@login_required
def document_update_old(request, id=None, template_name='wfpdocs/document_form.html'):
    wfpdoc = None
    content_type = None
    object_id = None
    if id:
        wfpdoc = get_object_or_404(WFPDocument, pk=id)
    if request.method == 'POST':
        if 'resource' in request.POST:
            resource = request.POST['resource']
            if resource != 'no_link':
                matches = re.match("type:(\d+)-id:(\d+)", resource).groups()
                contenttype_id = matches[0]
                object_id = matches[1]
                content_type = ContentType.objects.get(id=contenttype_id)
        title = request.POST['title']
        doc_file = None
        if 'file' in request.FILES:
            doc_file = request.FILES['file']
            if len(request.POST['title'])==0:
                return HttpResponse(_('You need to provide a document title.'))
            if not os.path.splitext(doc_file.name)[1].lower()[1:] in ALLOWED_DOC_TYPES:
                return HttpResponse(_('This file type is not allowed.'))
            if not doc_file.size < settings.MAX_DOCUMENT_SIZE * 1024 * 1024:
                return HttpResponse(_('This file is too big.'))
        else:
            if wfpdoc is None:
                return HttpResponse(_('You must provide a file.'))
        # map document
        form = WFPDocumentForm(request.POST)
        if form.is_valid():
            source = form.cleaned_data.get('source')
            publication_date = form.cleaned_data.get('publication_date')
            orientation = form.cleaned_data.get('orientation')
            page_format = form.cleaned_data.get('page_format')
            categories = form.cleaned_data.get('categories')
            regions = form.cleaned_data.get('regions')
            last_version = form.cleaned_data.get('last_version')
        if wfpdoc is None:
            wfpdoc = WFPDocument()
        wfpdoc.source = source
        wfpdoc.orientation = orientation
        wfpdoc.page_format = page_format
        wfpdoc.last_version = last_version
        # if we are creating the static map, we need to create the document as well
        if not id:
            document = Document(content_type=content_type, object_id=object_id, 
                title=title, doc_file=doc_file)
            document.owner = request.user
            document.save()
            wfpdoc.document = document
        else:
            document = wfpdoc.document
        # title=title, doc_file=doc_file, date=publication_date, regions=regions
        document.owner = request.user
        document.title = title
        if doc_file:
            document.doc_file = doc_file
        document.date = publication_date
        document.regions = regions
        document.content_type=content_type
        document.object_id=object_id
        document.save()
        document.update_thumbnail()
        #wfpdoc = WFPDocument(source = source, orientation=orientation,
        #    page_format=page_format, document=document)
        wfpdoc.save()
        wfpdoc.categories = categories
        # permissions
        if id is None:
            from geonode.documents.views import document_set_permissions
            permissionsStr = request.POST['permissions']
            permissions = json.loads(permissionsStr)
            document_set_permissions(document, permissions)
        return HttpResponseRedirect(reverse('wfpdocs-browse'))
    else: # GET
        if wfpdoc:
            form = WFPDocumentForm(instance=wfpdoc, 
                initial={'regions': wfpdoc.document.regions.all()})
        else:
            form = WFPDocumentForm()
        # some field in the form must be manually populated
        return render_to_response(
            'wfpdocs/document_form.html',
            { 'form': form,
            },
            RequestContext(request)
        )
        
@login_required
def document_remove(request, docid, template='wfpdocs/document_remove.html'):
    document = _resolve_document(request, docid, 'documents.delete_document',
                           _PERMISSION_MSG_DELETE)

    if request.method == 'GET':
        return render_to_response(template,RequestContext(request, {
            "document": document
        }))
    if request.method == 'POST':
        document.delete()
        return HttpResponseRedirect(reverse("wfpdocs-browse"))
    else:
        return HttpResponse("Not allowed",status=403)
