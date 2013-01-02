from pyramid.view import view_config
from formencode import Schema, validators
from pyramid_simpleform import Form
from pyramid_simpleform.renderers import FormRenderer
from amazonproduct import API


class ModelSchema(Schema):
    
    filter_extra_fields = True
    allow_extra_fields = True
    text = validators.MinLength(5, not_empty=True)


@view_config(route_name='home', renderer='templates/template.pt')
def my_view(request):
    form = Form(request, schema=ModelSchema)
    return dict(title = 'AmazoneBooks',renderer=FormRenderer(form))


@view_config(route_name = 'search',renderer='templates/template.pt')
def search_view(request):
    if request.method == 'POST':
        form = Form(request, schema=ModelSchema)
        print form
        AWS_KEY = 'AKIAINFQGAWKSGFXLOVA'
        SECRET_KEY = '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'
        AssTag = 'victor073-20'
        print ('1')
        i = 0
        api = API(AWS_KEY,SECRET_KEY,'uk',AssTag)
        print ('2')
        print ('3')
        for page in api.item_search('Books',Keywords=request.POST['text'],limit = 10):
            i+=1
            print i
            for book in page.Items.Item:
                if hasattr(book.ItemAttributes, 'Author'):
                    print(book.ItemAttributes.Author ,book.ItemAttributes.Title)
        print'4'
        return dict(title = request.POST['text'],renderer=FormRenderer(form))
    else:
        pass
