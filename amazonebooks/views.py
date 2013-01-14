from pyramid.view import view_config
from formencode import Schema, validators
from pyramid_simpleform import Form
from pyramid.response import Response
from pyramid_simpleform.renderers import FormRenderer
from lxml import etree
from amazon.api import AmazonAPI



class ModelSchema(Schema):
    
    filter_extra_fields = True
    allow_extra_fields = True
    text = validators.MinLength(5, not_empty=True)


def removeNonAscii(s): 
    return "".join(filter(lambda x: ord(x)<128, s))



@view_config(route_name='home', renderer='templates/template.pt')
def my_view(request):
    form = Form(request, schema=ModelSchema)
    return dict(title = 'AmazoneBooks',renderer=FormRenderer(form),booklist=[],css_url= './templates/style.css')



@view_config(route_name = 'search',renderer='templates/template.pt')
def search_view(request):
    #try:
        if request.method == 'POST':
            form = Form(request, schema=ModelSchema)
            AWS_KEY = 'AKIAINFQGAWKSGFXLOVA'
            SECRET_KEY = '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'
            AssTag = 'victor073-20'
            api = AmazonAPI(AWS_KEY,SECRET_KEY,AssTag,region='UK')
            booklist = []
            i = 0
            if request.POST['text']:
                books = api.search(Keywords=request.POST['text'], SearchIndex='Books')
                for n,book in enumerate(books):
                    booklist.append([])
                    if hasattr(book.item.ItemAttributes, 'Author'):
                        booklist[i].append('Author: ' + removeNonAscii(book.item.ItemAttributes.Author.__str__()))
                    else:
                        booklist[i].append('Author: -')
                    if hasattr(book.item.ItemAttributes, 'Title'):
                        booklist[i].append('Title: ' + removeNonAscii(book.item.ItemAttributes.Title.__str__()))
                    else:
                        booklist[i].append('Title: -')
                    if hasattr(book.item.ItemAttributes, 'Publisher'):
                        booklist[i].append("Publisher: " + removeNonAscii(book.item.ItemAttributes.Publisher.__str__()))
                    else:
                        booklist[i].append("Publisher: -")
                    c = api.lookup(ItemId=book.asin)
                    if hasattr(book.item, 'SmallImage'):
                        booklist[i].append(removeNonAscii(book.item.SmallImage.URL.__str__()))
                    else:
                        booklist[i].append("-")
                    if hasattr(book.item, 'LargeImage'):
                        booklist[i].append(removeNonAscii(book.item.LargeImage.URL.__str__()))
                    else:
                        booklist[i].append("-")
                    if hasattr(book.item, 'DetailPageURL'):
                        booklist[i].append(removeNonAscii(book.item.DetailPageURL.__str__()))
                    else:
                        booklist[i].append("-")
                    i+=1
                    print book.item.__dict__
            else:
                return dict(title = 'AmazoneBooks',renderer=FormRenderer(form),booklist=[])
            return dict(title = request.POST['text'],renderer=FormRenderer(form),booklist=booklist,css_url= './templates/style.css')
        else:
            pass
    #except NoExactMatchesFound:
 	return Response("ERROR. No such item")




