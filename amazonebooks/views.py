from pyramid.view import view_config
from formencode import Schema, validators
from pyramid_simpleform import Form
from pyramid.response import Response
from pyramid_simpleform.renderers import FormRenderer
from amazonproduct import API
from amazonproduct.errors import *


class ModelSchema(Schema):
    
    filter_extra_fields = True
    allow_extra_fields = True
    text = validators.MinLength(5, not_empty=True)


@view_config(route_name='home', renderer='templates/template.pt')
def my_view(request):
    form = Form(request, schema=ModelSchema)
    return dict(title = 'AmazoneBooks',renderer=FormRenderer(form),booklist=[])

def removeNonAscii(s): 
    return "".join(filter(lambda x: ord(x)<128, s))


@view_config(route_name = 'search',renderer='templates/template.pt')
def search_view(request):
    try:
        if request.method == 'POST':
            form = Form(request, schema=ModelSchema)
            AWS_KEY = 'AKIAINFQGAWKSGFXLOVA'
            SECRET_KEY = '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'
            AssTag = 'victor073-20'
            api = API(AWS_KEY,SECRET_KEY,'uk',AssTag)
            booklist = []
            i = 0
            if request.POST['text']:
                for page in api.item_search('Books',Keywords=request.POST['text'],limit = 10):
                    for book in page.Items.Item:
                        booklist.append([])
                        if hasattr(book.ItemAttributes, 'Author'):
                            booklist[i] = removeNonAscii(book.ItemAttributes.Author.__str__()) + ' '
                        if hasattr(book.ItemAttributes, 'Title'):
                            booklist[i]+=removeNonAscii(book.ItemAttributes.Title.__str__()) + ' '
                        if hasattr(book.ItemAttributes, 'Manufacturer'):
                            booklist[i]+=removeNonAscii(book.ItemAttributes.Manufacturer.__str__())
                        i+=1
            else:
                return dict(title = 'AmazoneBooks',renderer=FormRenderer(form))
            return dict(title = request.POST['text'],renderer=FormRenderer(form),booklist=booklist)
        else:
            pass
    except NoExactMatchesFound:
 	return Response("ERROR. No such item")
            
