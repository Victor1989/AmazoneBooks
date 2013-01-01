from pyramid.view import view_config
from formencode import Schema, validators
from pyramid_simpleform import Form
from pyramid_simpleform.renderers import FormRenderer
from amazonproduct import API


class ModelSchema(Schema):
    
    filter_extra_fields = True
    allow_extra_fields = True
    text = validators.MinLength(5, not_empty=True)

class MyModel(object):

    pass


@view_config(route_name='home', renderer='templates/template.pt')
def my_view(request):
    #item_id = request.matchdict['item_id']
    #item = session.query(MyModel).get(item_id)
    AWS_KEY = 'AKIAINFQGAWKSGFXLOVA'
    SECRET_KEY = '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'
    AssTag = 'victor073-20'
    print ('1')
    api = API(AWS_KEY,SECRET_KEY,'uk',AssTag)
    print ('2')
    #node = api.item_search('Books', Title='11 22 63')
    print ('3')
    for page in api.item_search('Books', Title='11 22 63'):
        for book in page.Items.Item:
            if hasattr(book.ItemAttributes, 'Author'):
                print(book.ItemAttributes.Author)
    form = Form(request, schema=ModelSchema)
    if form.validate():

        form.bind(MyModel)

        return HTTPFound(location="/")
    return dict(renderer=FormRenderer(form))


@view_config(route_name = 'search')
def search_view(request):
    AWS_KEY = 'AKIAINFQGAWKSGFXLOVA'
    SECRET_KEY = '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'
    print ('1')
    api = API('uk')
    print ('2')
    node = api.item_search('Books', Publisher='Galileo Press')
    print ('3')
