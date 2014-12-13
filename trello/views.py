from django.http import Http404, HttpResponse
from django.shortcuts import render
from trello.models import Board

def display_overview(request):
    boards = Board.objects
    count = boards.count()
    board_list = boards.all()
    return render(request, 'overview.html', {
        'nboards': count,
        'boards': board_list,
    })

def display_board(request, board_id):
    return render(request, 'board.html', {'id': board_id})
