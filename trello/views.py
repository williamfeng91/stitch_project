from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from trello.models import *

def home(request):
    boards = Board.objects
    count = boards.count()
    board_list = boards.all()
    return render(request, 'overview.html', {
        'nboards': count,
        'boards': board_list,
    })

def board(request, board_id):
    try:
        board = Board.objects.get(id=board_id)
    except Board.DoesNotExist:
        raise Http404()
    lists = List.objects
    count = lists.count()
    list_list = lists.all()
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
    return render(request, 'list.html', {
        'deletion_error': False,
        'board_id': board_id,
        'list': list,
    })

def new_list(request, board_id):
    return render(request, 'new_list.html', {
        'board_id': board_id,
    })

def request_handler(request):
    if 'add_board' in request.POST and request.POST['add_board']:
        b = Board(name=request.POST['add_board'])
        b.save()
    elif 'delete_board' in request.POST and request.POST['delete_board']:
        try:
            b = Board.objects.get(id=request.POST['delete_board'])
            b.delete()
        except Board.DoesNotExist:
            pass
    elif 'add_list' in request.POST and request.POST['add_list']:
        board = request.POST['board_id'];
        l = List(
            name=request.POST['add_list'],
            board_id=board,
        )
        l.save()
        redirect_url='/Boards/%s/' % (board)
        return HttpResponseRedirect(redirect_url)
    elif 'delete_list' in request.POST and request.POST['delete_list']:
        try:
            l = List.objects.get(id=request.POST['delete_list'])
            l.delete()
        except List.DoesNotExist:
            pass
        redirect_url='/Boards/%s/' % (request.POST['board_id'])
        return HttpResponseRedirect(redirect_url)
    else:
        raise Http404()
    return HttpResponseRedirect('/')
