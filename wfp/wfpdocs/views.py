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

from geonode.utils import resolve_object
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
    wfpdoc = WFPDocument.objects.get(slug=slug)
    return resolve_object(request, WFPDocument, {'pk': wfpdoc.id},
                          permission=permission, permission_msg=msg, **kwargs)

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


def document_download(request, slug):
    document = get_object_or_404(WFPDocument, slug=slug)
    if not request.user.has_perm(
            'base.download_resourcebase',
            obj=document.get_self_resource()):
        return HttpResponse(
            loader.render_to_string(
                '401.html', RequestContext(
                    request, {
                        'error_message': _("You are not allowed to view this document.")})), status=401)
    return DownloadResponse(document.doc_file)


class DocumentUploadView(CreateView):
    model = WFPDocument
    form_class = WFPDocumentForm
    
    def form_valid(self, form):
        """
        If the form is valid, save the associated model.
        """
        self.object = form.save(commit=False)
        self.object.owner = self.request.user
        # by default, if RESOURCE_PUBLISHING=True then document.is_published
        # must be set to False
        is_published = True
        if settings.RESOURCE_PUBLISHING:
            is_published = False
        self.object.is_published = is_published
        self.object.save()
        self.object.set_permissions(form.cleaned_data['permissions'])
        return HttpResponseRedirect(
            reverse(
                'wfpdocs_detail',
                args=(
                    self.object.slug,
                )))


class DocumentUpdateView(UpdateView):
    model = WFPDocument
    form_class = WFPDocumentForm
                
        
@login_required
def document_remove(request, slug, template='wfpdocs/document_remove.html'):
    try:
        document = _resolve_document(
            request,
            slug,
            'base.delete_resourcebase',
            _PERMISSION_MSG_DELETE)

        if request.method == 'GET':
            return render_to_response(template, RequestContext(request, {
                "document": document
            }))
        if request.method == 'POST':
            document.delete()
            return HttpResponseRedirect(reverse("wfpdocs_browse"))
        else:
            return HttpResponse("Not allowed", status=403)

    except PermissionDenied:
        return HttpResponse(
            'You are not allowed to delete this document',
            mimetype="text/plain",
            status=401
        )
