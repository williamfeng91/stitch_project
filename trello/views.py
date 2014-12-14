from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from trello.models import *

# display home page
def home(request):
    board_list = Board.objects.all() # all boards
    count = board_list.count()
    return render(request, 'overview.html', {
        'nboards': count,
        'boards': board_list,
    })

# display board
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

# display page for creation of new board
def new_board(request):
    return render(request, 'new_board.html')

# display list
def list(request, board_id, list_id):
    try:
        list = List.objects.get(id=list_id)
    except List.DoesNotExist:
        raise Http404()
    card_list = Card.objects.filter(list_id=list_id) # all cards in the current list
    count = card_list.count()
    return render(request, 'list.html', {
        'board_id': board_id,
        'list': list,
        'ncards': count,
        'cards': card_list,
    })

# display page for creation of new list
def new_list(request, board_id):
    return render(request, 'new_list.html', {
        'board_id': board_id,
    })

# display card
def card(request, board_id, list_id, card_id):
    try:
        card = Card.objects.get(id=card_id)
    except Card.DoesNotExist:
        raise Http404()
    label_list = Label.objects.filter(board_id=board_id) # all labels in the current board
    label_count = label_list.count() # number of labels in the current board, used to check maximum of 6 labels in the template
    list_list = List.objects.filter(board_id=board_id).order_by('name') # all lists in the current board that the current card can be moved to
    member_list = Member.objects.order_by('name') # all members that can be assigned to the current card
    participating_members = card.member_set.all() # members already assigned to the current card
    member_count = participating_members.count()
    label = None
    try:
        label = label_list.get(card_id=card_id) # check if there is a label on the current card
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

# display page for creation of new card
def new_card(request, board_id, list_id):
    return render(request, 'new_card.html', {
        'board_id': board_id,
        'list_id': list_id,
    })

# display page for creation of new label
def new_label(request, board_id, list_id, card_id):
    return render(request, 'new_label.html', {
        'board_id': board_id,
        'list_id': list_id,
        'card_id': card_id,
    })

# display all members
def members(request):
    member_list = Member.objects.all()
    count = member_list.count()
    return render(request, 'members.html', {
        'nmembers': count,
        'members': member_list,
    })

# display member profile
def member(request, member_id):
    try:
        member = Member.objects.get(id=member_id)
    except Member.DoesNotExist:
        raise Http404()
    return render(request, 'member.html', {
        'member': member,
    })

# display page for creation of new member
def new_member(request):
    return render(request, 'new_member.html')

# handle requests to modify the database
def request_handler(request):
    if 'add_board' in request.POST:

        # handle request to add a new board
        # check name constraints
        if request.POST['board_name'] and len(request.POST['board_name']) <= 30:
            b = Board(name=request.POST['board_name'])
            b.save()
        # redirect to home page
        return HttpResponseRedirect('/')
    elif 'delete_board' in request.POST:

        # handle request to delete a board
        try:
            b = Board.objects.get(id=request.POST['board_id'])
            b.delete()
        except Board.DoesNotExist:
            pass
        # redirect to home page
        return HttpResponseRedirect('/')
    elif 'rename_board' in request.POST:

        # handle request to rename a board
        # check name constraints
        if request.POST['board_name'] and len(request.POST['board_name']) <= 30:
            try:
                b = Board.objects.get(id=request.POST['board_id'])
                b.name = request.POST['board_name']
                b.save()
            except Board.DoesNotExist:
                pass
        # redirect to the current board
        redirect_url='/Boards/%s/' % (
            request.POST['board_id'],
        )
        return HttpResponseRedirect(redirect_url)
    elif 'add_list' in request.POST:

        # handle request to add a new list
        # check name constraints
        if request.POST['list_name'] and len(request.POST['list_name']) <= 30:
            l = List(
                name=request.POST['list_name'],
                board_id=request.POST['board_id'],
            )
            l.save()
        # redirect to the current board
        redirect_url='/Boards/%s/' % (
            request.POST['board_id'],
        )
        return HttpResponseRedirect(redirect_url)
    elif 'delete_list' in request.POST:

        # handle request to delete a list
        try:
            l = List.objects.get(id=request.POST['list_id'])
            l.delete()
        except List.DoesNotExist:
            pass
        # redirect to the current board
        redirect_url='/Boards/%s/' % (
            request.POST['board_id'],
        )
        return HttpResponseRedirect(redirect_url)
    elif 'rename_list' in request.POST:

        # handle request to rename a list
        # check name constraints
        if request.POST['list_name'] and len(request.POST['list_name']) <= 30:
            try:
                l = List.objects.get(id=request.POST['list_id'])
                l.name = request.POST['list_name']
                l.save()
            except List.DoesNotExist:
                pass
        # redirect to the current list
        redirect_url='/Boards/%s/Lists/%s/' % (
            request.POST['board_id'],
            request.POST['list_id'],
        )
        return HttpResponseRedirect(redirect_url)
    elif 'add_card' in request.POST:

        # handle request to add a new card
        # check card constraints
        if request.POST['card_title'] and len(request.POST['card_title']) <= 30 and len(request.POST['description']) <= 100 and request.POST['due_date'] and request.POST['list_id']:
            c = Card(
                title=request.POST['card_title'],
                description=request.POST['description'],
                due_date=request.POST['due_date'],
                list_id=request.POST['list_id'],
            )
            c.save()
        # redirect to the current list
        redirect_url='/Boards/%s/Lists/%s/' % (
            request.POST['board_id'],
            request.POST['list_id'],
        )
        return HttpResponseRedirect(redirect_url)
    elif 'delete_card' in request.POST:

        # handle request to delete a card
        try:
            c = Card.objects.get(id=request.POST['card_id'])
            c.delete()
        except Card.DoesNotExist:
            pass
        # redirect to the current list
        redirect_url='/Boards/%s/Lists/%s/' % (
            request.POST['board_id'],
            request.POST['list_id'],
        )
        return HttpResponseRedirect(redirect_url)
    elif 'edit_card' in request.POST:

        # handle request to edit a card
        try:
            c = Card.objects.get(id=request.POST['card_id'])
            if request.POST['card_title'] and len(request.POST['card_title']) <= 30:
                c.title = request.POST['card_title']
            if len(request.POST['card_description']) <= 100:
                c.description = request.POST['card_description']
            if request.POST['card_due_date']:
                c.due_date = request.POST['card_due_date']
            if request.POST['moveTo'] and request.POST['moveTo'] != c.list_id:
                c.list_id = request.POST['moveTo']
            c.save()
        except Card.DoesNotExist:
            pass
        # redirect to the current card
        redirect_url='/Boards/%s/Lists/%s/Cards/%s/' % (
            request.POST['board_id'],
            c.list_id,
            request.POST['card_id'],
        )
        return HttpResponseRedirect(redirect_url)
    elif 'add_label' in request.POST:

        # handle request to add a new label
        # check name constraints
        if request.POST['label_name'] and len(request.POST['label_name']) <= 30:
            lb = Label(
                name=request.POST['label_name'],
                board_id=request.POST['board_id'],
                card_id=request.POST['card_id'],
            )
            lb.save()
        # redirect to the current card
        redirect_url='/Boards/%s/Lists/%s/Cards/%s/' % (
            request.POST['board_id'],
            request.POST['list_id'],
            request.POST['card_id'],
        )
        return HttpResponseRedirect(redirect_url)
    elif 'delete_label' in request.POST:

        # handle request to delete a label
        try:
            lb = Label.objects.get(id=request.POST['label_id'])
            lb.delete()
        except Label.DoesNotExist:
            pass
        # redirect to the current card
        redirect_url='/Boards/%s/Lists/%s/Cards/%s/' % (
            request.POST['board_id'],
            request.POST['list_id'],
            request.POST['card_id'],
        )
        return HttpResponseRedirect(redirect_url)
    elif 'rename_label' in request.POST:

        # handle request to rename a label
        # check name constraints
        if request.POST['label_name'] and len(request.POST['label_name']) <= 30:
            try:
                lb = Label.objects.get(id=request.POST['label_id'])
                lb.name = request.POST['label_name']
                lb.save()
            except Label.DoesNotExist:
                pass
        # redirect to the current card
        redirect_url='/Boards/%s/Lists/%s/Cards/%s/' % (
            request.POST['board_id'],
            request.POST['list_id'],
            request.POST['card_id'],
        )
        return HttpResponseRedirect(redirect_url)
    elif 'add_member' in request.POST:

        # handle request to add a new member
        # check name constraints
        if request.POST['member_name'] and len(request.POST['member_name']) <= 70:
            m = Member(name=request.POST['member_name'])
            m.save()
        # redirect to the member list page
        redirect_url='/Members/'
        return HttpResponseRedirect(redirect_url)
    elif 'delete_member' in request.POST:

        # handle request to delete a member
        try:
            m = Member.objects.get(id=request.POST['member_id'])
            m.delete()
        except Member.DoesNotExist:
            pass
        # redirect to the member list page
        redirect_url='/Members/'
        return HttpResponseRedirect(redirect_url)
    elif 'rename_member' in request.POST:

        # handle request to rename a member
        # check name constraints
        if request.POST['member_name'] and len(request.POST['member_name']) <= 70:
            try:
                m = Member.objects.get(id=request.POST['member_id'])
                m.name = request.POST['member_name']
                m.save()
            except Member.DoesNotExist:
                pass
        # redirect to the member profile page
        redirect_url='/Members/%s/' % (
            request.POST['member_id'],
        )
        return HttpResponseRedirect(redirect_url)
    elif 'assign_member' in request.POST:

        # handle request to assign a member to a card
        try:
            m = Member.objects.get(id=request.POST['new_member'])
            c = Card.objects.get(id=request.POST['card_id'])
            m.card.add(c)
            c.member_set.add(m)
        except Member.DoesNotExist:
            pass
        except Card.DoesNotExist:
            pass
        # redirect to the current card
        redirect_url='/Boards/%s/Lists/%s/Cards/%s/' % (
            request.POST['board_id'],
            request.POST['list_id'],
            request.POST['card_id'],
        )
        return HttpResponseRedirect(redirect_url)
    elif 'list_up' in request.POST:

        # handle request to move a list up
        try:
            id1 = request.POST['list_id']
            l1 = List.objects.get(id=id1)
            index2 = List.objects.filter(board=request.POST['board_id']).filter(id__lt=id1).count() - 1 # index of the list above
            if index2 >= 0: # if l1 is not at the top, swap id with the list above
                l2 = List.objects.all()[index2]
                id2 = l2.id
                l1.id = id2
                l2.id = id1
                l1.save()
                l2.save()
        except List.DoesNotExist:
            pass
        # redirect to the current board
        redirect_url='/Boards/%s/' % (
            request.POST['board_id'],
        )
        return HttpResponseRedirect(redirect_url)
    elif 'list_down' in request.POST:

        # handle request to move a list down
        try:
            id1 = request.POST['list_id']
            l1 = List.objects.get(id=id1)
            l = List.objects.filter(board=request.POST['board_id']).filter(id__gt=id1) # all lists below l1
            if l.count() > 0: # if l1 is not at the bottom, swap id with the list below
                l2 = l[0]
                id2 = l2.id
                l1.id = id2
                l2.id = id1
                l1.save()
                l2.save()
        except List.DoesNotExist:
            pass
        # redirect to the current board
        redirect_url='/Boards/%s/' % (
            request.POST['board_id'],
        )
        return HttpResponseRedirect(redirect_url)
    elif 'card_up' in request.POST:

        # handle request to move a card up
        try:
            id1 = request.POST['card_id']
            c1 = Card.objects.get(id=id1)
            index2 = Card.objects.filter(list=request.POST['list_id']).filter(id__lt=id1).count() - 1 # index of the card above
            if index2 >= 0: # if c1 is not at the top, swap id with the card above
                c2 = Card.objects.all()[index2]
                id2 = c2.id
                c1.id = id2
                c2.id = id1
                c1.save()
                c2.save()
        except Card.DoesNotExist:
            pass
        # redirect to the current list
        redirect_url='/Boards/%s/Lists/%s/' % (
            request.POST['board_id'],
            request.POST['list_id'],
        )
        return HttpResponseRedirect(redirect_url)
    elif 'card_down' in request.POST:

        # handle request to move a card down
        try:
            id1 = request.POST['card_id']
            c1 = Card.objects.get(id=id1)
            c = Card.objects.filter(list=request.POST['list_id']).filter(id__gt=id1) # all cards below c1
            if c.count() > 0: # if c1 is not at the bottom, swap id with the card below
                c2 = c[0]
                id2 = c2.id
                c1.id = id2
                c2.id = id1
                c1.save()
                c2.save()
        except Card.DoesNotExist:
            pass
        # redirect to the current list
        redirect_url='/Boards/%s/Lists/%s/' % (
            request.POST['board_id'],
            request.POST['list_id'],
        )
        return HttpResponseRedirect(redirect_url)
    else:

        # unknown request
        raise Http404()
    return HttpResponseRedirect('/')
