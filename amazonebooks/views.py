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
    AWS_KEY = 'AKIAIBKTKJFSLKCXYBYA'
    SECRET_KEY = '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'
    api = API(AWS_KEY, SECRET_KEY, 'us')
    node = api.item_search('Books', Publisher='Galileo Press')
    form = Form(request, schema=ModelSchema)
    if form.validate():

        form.bind(MyModel)

        return HTTPFound(location="/")
    return dict(renderer=FormRenderer(form))
