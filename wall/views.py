from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from wall.models import Wall, WallItem
from wall.forms import WallItemForm

def home( request, slug, template_name='wall/home.html'):
    """
    A view that shows all of the wall items.
    (Use template_name of 'wall/recent.html' to see just recent items.)
    """
    wall = get_object_or_404( Wall, slug=slug )

    return render_to_response( template_name,
        {   "wall": wall,
            "form": WallItemForm()
        },
        context_instance = RequestContext( request ))

@login_required
def add( request, slug, form_class=WallItemForm,
            template_name='wall/add.html',
            success_url=None, can_add_check=None):
    """
    A view for adding a new WallItem.

    The optional 'can_add_check' callback passes you a user and a wall.
      Return True if the user is authorized and False otherwise.
      (Default: any user can create a wall item for the given wall.)
    """
    wall = get_object_or_404( Wall, slug=slug )
    if success_url == None:
        success_url = reverse( 'wall_home', args=(slug,))
    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            posting = form.cleaned_data['posting']
            if len(posting) > wall.max_item_length:
                body = posting[:wall.max_item_length]
            else:
                body = posting
            item = WallItem( author=request.user, wall=wall, body=body )
            item.save()
            return HttpResponseRedirect(success_url)
    else:
        if can_add_check != None:
            allowed = can_add_check( request.user, wall )
        else:
            allowed = True
        if not allowed:
            request.user.message_set.create(
                message='You do not have permission to add an item to this wall.')
            return HttpResponseRedirect(success_url)
        form = form_class( help_text="Input text for a new item.<br/>(HTML tags will %sbe ignored. The item will be trimmed to %d characters.)" % ("not " if wall.allow_html else "", wall.max_item_length))
    return render_to_response(template_name,
        { 'form': form, 'wall': wall },
        context_instance = RequestContext( request ))

@login_required
def edit( request, id, form_class=WallItemForm,
            template_name='wall/edit.html',
            success_url=None, can_edit_check=None):
    """
    A view for editing a WallItem.

    The optional 'can_edit_check' callback passes you a user and an item.
      Return True if the user is authorized and False otherwise.
      (Default: only the item author is allowed to edit the item.)
    """
    item = get_object_or_404( WallItem, id=int(id) )
    if success_url == None:
        success_url = reverse( 'wall_home', args=(item.wall.slug,))
    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            posting = form.cleaned_data['posting']
            if len(posting) > item.wall.max_item_length:
                body = posting[:item.wall.max_item_length]
            else:
                body = posting       
            item.body = body
            item.save()
            return HttpResponseRedirect(success_url)
    else:
        if can_edit_check != None:
            allowed = can_edit_check( request.user, item )
        else:
            allowed = (request.user == item.author)
        if not allowed:
            request.user.message_set.create(
                message='You do not have permission to edit that item.')
            return HttpResponseRedirect(success_url)
        form = form_class( help_text="Edit this item.<br/>(HTML tags will %sbe ignored. The item will be trimmed to %d characters.)" % ("not " if item.wall.allow_html else "", item.wall.max_item_length))
        form.fields['posting'].initial = item.body
    return render_to_response(template_name,
        { 'form': form, 'item': item, 'wall': item.wall },
        context_instance = RequestContext( request ))

