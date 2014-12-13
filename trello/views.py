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
    if 'add_board_name' in request.POST and request.POST['add_board_name']:
        new_board = Board(name=request.POST['add_board_name'])
        new_board.save()
    else:
        raise Http404()
    return HttpResponseRedirect('/')
