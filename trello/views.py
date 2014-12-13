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
    label_count = label_list.count()
    label = None
    list_list = List.objects.filter(board_id=board_id).order_by('name')
    member_list = Member.objects.order_by('name')
    participating_members = card.member_set.all()
    member_count = participating_members.count()
    try:
        label = label_list.get(card_id=card_id)
        hasLabel = True
    except Label.DoesNotExist:
        hasLabel = False
    return render(request, 'card.html', {
        'board_id': board_id,
        'list_id': list_id,
        'card': card,
        'nlabels': label_count,
        'hasLabel': hasLabel,
        'label': label,
        'lists': list_list,
        'nmembers': member_count,
        'members': participating_members,
        'all_members': member_list,
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

def members(request):
    member_list = Member.objects.all()
    count = member_list.count()
    return render(request, 'members.html', {
        'nmembers': count,
        'members': member_list,
    })

def member(request, member_id):
    try:
        member = Member.objects.get(id=member_id)
    except Member.DoesNotExist:
        raise Http404()
    return render(request, 'member.html', {
        'member': member,
    })

def new_member(request):
    return render(request, 'new_member.html')

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
    elif 'edit_card' in request.POST and request.POST['card_id'] and request.POST['card_title']:
        try:
            c = Card.objects.get(id=request.POST['card_id'])
            c.title = request.POST['card_title']
            c.description = request.POST['card_description']
            if request.POST['card_due_date']:
                c.due_date = request.POST['card_due_date']
            if request.POST['moveTo'] and request.POST['moveTo'] != c.list_id:
                c.list_id = request.POST['moveTo']
            c.save()
        except Card.DoesNotExist:
            pass
        redirect_url='/Boards/%s/Lists/%s/Cards/%s/' % (
            request.POST['board_id'],
            c.list_id,
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
    elif 'add_member' in request.POST and request.POST['add_member']:
        m = Member(name=request.POST['add_member'])
        m.save()
        redirect_url='/Members/'
        return HttpResponseRedirect(redirect_url)
    elif 'delete_member' in request.POST and request.POST['member_id']:
        try:
            m = Member.objects.get(id=request.POST['member_id'])
            m.delete()
        except Member.DoesNotExist:
            pass
        redirect_url='/Members/'
        return HttpResponseRedirect(redirect_url)
    elif 'rename_member' in request.POST and request.POST['member_id'] and request.POST['member_name']:
        try:
            m = Member.objects.get(id=request.POST['member_id'])
            m.name = request.POST['member_name']
            m.save()
        except Member.DoesNotExist:
            pass
        redirect_url='/Members/%s/' % (
            request.POST['member_id'])
        return HttpResponseRedirect(redirect_url)
    elif 'assign_member' in request.POST and request.POST['new_member']:
        try:
            m = Member.objects.get(id=request.POST['new_member'])
            c = Card.objects.get(id=request.POST['card_id'])
            m.card.add(c)
            c.member_set.add(m)
        except Member.DoesNotExist:
            pass
        except Card.DoesNotExist:
            pass
        redirect_url='/Boards/%s/Lists/%s/Cards/%s/' % (
            request.POST['board_id'],
            request.POST['list_id'],
            request.POST['card_id'])
        return HttpResponseRedirect(redirect_url)
    else:
        raise Http404()
    return HttpResponseRedirect('/')
