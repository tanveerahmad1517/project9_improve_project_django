from django.db.models import Q
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404
from django.utils import timezone

from . import models
from . import forms


def menu_list(request):
    """Shows the list of all menus with the missing expiration date or
    expiration date in the future."""
    today = timezone.now().date()
    menus = models.Menu.objects.prefetch_related('items').filter(
        Q(expiration_date__gte=today) | Q(expiration_date__isnull=True)
    ).order_by('expiration_date')
    return render(request, 'menu/list_all_current_menus.html', {
        'menus': menus})


def menu_detail(request, pk):
    """Shows menu details if menu exists."""
    try:
        menu = models.Menu.objects.prefetch_related('items').get(pk=pk)
    except models.Menu.DoesNotExist:
        raise Http404
    return render(request, 'menu/menu_detail.html', {'menu': menu})


def item_detail(request, pk):
    """Shows item details if item exists."""
    try:
        item = models.Item.objects.select_related('chef').prefetch_related(
            'ingredients').get(pk=pk)
    except models.Menu.DoesNotExist:
        raise Http404
    return render(request, 'menu/detail_item.html', {'item': item})


def menu_create_edit(request, pk=0):
    """View to add new or edit existing menu."""
    try:
        menu = models.Menu.objects.get(pk=pk)
    except models.Menu.DoesNotExist:
        menu = None
    form = forms.MenuForm(instance=menu)

    if request.method == 'POST':
        form = forms.MenuForm(instance=menu, data=request.POST)
        if form.is_valid():
            if menu:
                for item in menu.items.all():
                    item.items.remove(menu)
                form.save()
            else:
                menu = form.save()
            for item in menu.items.all():
                item.items.add(menu)
            return HttpResponseRedirect(
                reverse('menu:detail', kwargs={'pk': menu.pk}))
    return render(request, 'menu/menu_edit.html', {'form': form})
