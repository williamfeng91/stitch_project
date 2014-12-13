from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from trello.models import Board

def home(request):
    boards = Board.objects
    count = boards.count()
    board_list = boards.all()
    return render(request, 'overview.html', {
        'nboards': count,
        'boards': board_list,
    })

def board(request, board_id):
    board = Board.objects.get(id=board_id)
    return render(request, 'board.html', {
        'board': board,
    })

def new_board(request):
    return render(request, 'new_board.html')

def request_handler(request):
    if 'add_board' in request.POST and request.POST['add_board']:
        b = Board(name=request.POST['add_board'])
        b.save()
    elif 'delete_board' in request.POST and request.POST['delete_board']:
        b = Board.objects.get(id=request.POST['delete_board'])
        b.delete()
    else:
        raise Http404()
    return HttpResponseRedirect('/')
