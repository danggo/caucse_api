from django.http import HttpResponse
from django.core import serializers
from django.utils.simplejson import dumps

from models import *
import datetime

# TODO: should separate logic from view

def users_show(request):
    id = request.GET['user_id']
    member = Member.objects.get(id=id)
    ret = serializers.serialize('json', [member], ensure_ascii=False)
    return HttpResponse(ret)
    
def users_lookup(request):
    id_list = request.GET['user_id'].split(',')
    members = [Member.objects.get(id=id) for id in id_list]
    ret = serializers.serialize('json', members, ensure_ascii=False)
    return HttpResponse(ret)
 
def boards_lookup(request):
    board_list = request.GET['board_id'].split(',')

    # lookup board information from board_id param.
    boardinfo = []
    for tablename in board_list:
        if tablename.startswith('board'):
            boardinfo.append(Boardinfo.objects.get(tablename=tablename))
        elif tablename.startswith('photo'):
            boardinfo.append(Photoinfo.objects.get(tablename=tablename))

    # compose data to make json
    boards = []
    for board in boardinfo:
        board_dict = {}
        classname = board.tablename.title().replace('_','')
        board_model = eval(classname)
        day_ago = datetime.datetime.today() - datetime.timedelta(days=1)
        
        board_dict['board_id'] = board.tablename
        board_dict['title'] = board.title
        board_dict['description'] = board.description
        board_dict['admin'] = board.admin_id
        board_dict['count'] = board_model.objects.count()
        board_dict['count_24h_ago'] = board_model.objects\
                                                 .filter(reg_date__gt=day_ago)\
                                                 .count()
        boards.append(board_dict)

    # return json object
    ret = dumps(boards, ensure_ascii=False)
    return HttpResponse(ret)

def boards_list(request):
    page = 0
    per_page = 20
    
    # get request parameter 
    board_id = request.GET['board_id']
    if request.GET.has_key('page'):
        page = int(request.GET['page'])
    if request.GET.has_key('per_page'):
        per_page = int(request.GET['per_page'])

    # prepare query parameter 
    start_index = page * per_page
    end_index = start_index + per_page
    classname = board_id.title().replace('_','')
    board_model = eval(classname)
    
    # compose data into list
    item_list = []
    articles = board_model.objects.all().order_by('-reg_date')
    for article in articles[start_index:end_index]:
        item_dict = {}
        item_dict['board_id'] = board_id
        item_dict['article_id'] = article.id
        item_dict['title'] = article.title
        item_dict['view_count'] = article.count
        # need to setup datetime timezone info
        item_dict['reg_date'] = article.reg_date.isoformat()
        item_dict['comment_count'] = article.comment
        if article.file_name:
            # TODO: should convert to url
            item_dict['filename'] = article.file_name
        item_list.append(item_dict)        

    # return JSON object 
    ret = dumps(item_list, ensure_ascii=False)
    return HttpResponse(ret)
