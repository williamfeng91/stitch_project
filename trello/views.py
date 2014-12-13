from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from trello.models import *

def home(request):
    board_list = Board.objects.all()
    count = board_list.count()
    return render(request, 'overview.html', {
        'nboards': count,
        'boards': board_list,
    })

def board(request, board_id):
    try:
        board = Board.objects.get(id=board_id)
    except Board.DoesNotExist:
        raise Http404()
    list_list = List.objects.filter(board_id=board_id)
    count = list_list.count()
    return render(request, 'board.html', {
        'board': board,
        'nlists': count,
        'lists': list_list,
    })

def new_board(request):
    return render(request, 'new_board.html')

def list(request, board_id, list_id):
    try:
        list = List.objects.get(id=list_id)
    except List.DoesNotExist:
        raise Http404()
    card_list = Card.objects.filter(list_id=list_id)
    count = card_list.count()
    return render(request, 'list.html', {
        'board_id': board_id,
        'list': list,
        'ncards': count,
        'cards': card_list,
    })

def new_list(request, board_id):
    return render(request, 'new_list.html', {
        'board_id': board_id,
    })

def card(request, board_id, list_id, card_id):
    try:
        card = Card.objects.get(id=card_id)
    except Card.DoesNotExist:
        raise Http404()
    label_list = Label.objects.filter(board_id=board_id)
    count = label_list.count()
    label = None
    try:
        label = label_list.get(card_id=card_id)
        hasLabel = True
    except Label.DoesNotExist:
        hasLabel = False
    return render(request, 'card.html', {
        'board_id': board_id,
        'list_id': list_id,
        'card': card,
        'nlabels': count,
        'hasLabel': hasLabel,
        'label': label,
    })

def new_card(request, board_id, list_id):
    return render(request, 'new_card.html', {
        'board_id': board_id,
        'list_id': list_id,
    })

def new_label(request, board_id, list_id, card_id):
    return render(request, 'new_label.html', {
        'board_id': board_id,
        'list_id': list_id,
        'card_id': card_id,
    })

def request_handler(request):
    if 'add_board' in request.POST and request.POST['add_board']:
        b = Board(name=request.POST['add_board'])
        b.save()
    elif 'delete_board' in request.POST and request.POST['board_id']:
        try:
            b = Board.objects.get(id=request.POST['board_id'])
            b.delete()
        except Board.DoesNotExist:
            pass
    elif 'rename_board' in request.POST and request.POST['board_id'] and request.POST['board_name']:
        try:
            b = Board.objects.get(id=request.POST['board_id'])
            b.name = request.POST['board_name']
            b.save()
        except Board.DoesNotExist:
            pass
        redirect_url='/Boards/%s/' % (
            request.POST['board_id'])
        return HttpResponseRedirect(redirect_url)
    elif 'add_list' in request.POST and request.POST['add_list']:
        board = request.POST['board_id'];
        l = List(
            name=request.POST['add_list'],
            board_id=board,
        )
        l.save()
        redirect_url='/Boards/%s/' % (board)
        return HttpResponseRedirect(redirect_url)
    elif 'delete_list' in request.POST and request.POST['list_id']:
        try:
            l = List.objects.get(id=request.POST['list_id'])
            l.delete()
        except List.DoesNotExist:
            pass
        redirect_url='/Boards/%s/' % (request.POST['board_id'])
        return HttpResponseRedirect(redirect_url)
    elif 'rename_list' in request.POST and request.POST['list_id'] and request.POST['list_name']:
        try:
            l = List.objects.get(id=request.POST['list_id'])
            l.name = request.POST['list_name']
            l.save()
        except List.DoesNotExist:
            pass
        redirect_url='/Boards/%s/Lists/%s/' % (
            request.POST['board_id'],
            request.POST['list_id'])
        return HttpResponseRedirect(redirect_url)
    elif 'add_card' in request.POST and request.POST['add_card']:
        c = Card(
            title=request.POST['add_card'],
            description=request.POST['description'],
            due_date=request.POST['due_date'],
            list_id=request.POST['list_id'],
        )
        c.save()
        redirect_url='/Boards/%s/Lists/%s/' % (
            request.POST['board_id'],
            request.POST['list_id'])
        return HttpResponseRedirect(redirect_url)
    elif 'delete_card' in request.POST and request.POST['card_id']:
        try:
            c = Card.objects.get(id=request.POST['card_id'])
            c.delete()
        except Card.DoesNotExist:
            pass
        redirect_url='/Boards/%s/Lists/%s/' % (
            request.POST['board_id'],
            request.POST['list_id'])
        return HttpResponseRedirect(redirect_url)
    elif 'change_card' in request.POST and request.POST['card_id'] and request.POST['card_title']:
        try:
            c = Card.objects.get(id=request.POST['card_id'])
            c.title = request.POST['card_title']
            c.description = request.POST['card_description']
            c.due_date = request.POST['card_due_date']
            c.save()
        except Card.DoesNotExist:
            pass
        redirect_url='/Boards/%s/Lists/%s/Cards/%s/' % (
            request.POST['board_id'],
            request.POST['list_id'],
            request.POST['card_id'])
        return HttpResponseRedirect(redirect_url)
    elif 'add_label' in request.POST and request.POST['add_label']:
        lb = Label(
            name=request.POST['add_label'],
            board_id=request.POST['board_id'],
            card_id=request.POST['card_id'],
        )
        lb.save()
        redirect_url='/Boards/%s/Lists/%s/Cards/%s/' % (
            request.POST['board_id'],
            request.POST['list_id'],
            request.POST['card_id'])
        return HttpResponseRedirect(redirect_url)
    elif 'delete_label' in request.POST and request.POST['label_id']:
        try:
            lb = Label.objects.get(id=request.POST['label_id'])
            lb.delete()
        except Label.DoesNotExist:
            pass
        redirect_url='/Boards/%s/Lists/%s/Cards/%s/' % (
            request.POST['board_id'],
            request.POST['list_id'],
            request.POST['card_id'])
        return HttpResponseRedirect(redirect_url)
    elif 'rename_label' in request.POST and request.POST['label_id'] and request.POST['label_name']:
        try:
            lb = Label.objects.get(id=request.POST['label_id'])
            lb.name = request.POST['label_name']
            lb.save()
        except Label.DoesNotExist:
            pass
        redirect_url='/Boards/%s/Lists/%s/Cards/%s/' % (
            request.POST['board_id'],
            request.POST['list_id'],
            request.POST['card_id'])
        return HttpResponseRedirect(redirect_url)
    else:
        raise Http404()
    return HttpResponseRedirect('/')
