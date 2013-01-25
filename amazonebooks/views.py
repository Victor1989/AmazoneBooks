import sys

import sqlite3 as lite

from lxml import etree

from pyramid.view import view_config
from formencode import Schema, validators
from pyramid_simpleform import Form
from pyramid.response import Response
from pyramid_simpleform.renderers import FormRenderer
from amazon.api import AmazonAPI





AWS_KEY = 'AKIAINFQGAWKSGFXLOVA'
SECRET_KEY = '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'
AssTag = 'victor073-20'
api = AmazonAPI(AWS_KEY, SECRET_KEY, AssTag, region='UK')



class ModelSchema(Schema):
    
    # schema for the form
    
    filter_extra_fields = True
    allow_extra_fields = True
    text = validators.MinLength(5, not_empty=True)


def removeNonAscii(s): 
    return "".join(filter(lambda x: ord(x) < 128, s))


def read_database(asin):
    con = None

    try:
        con = lite.connect('./amazonebooks/Likes.db')
        cur = con.cursor()
        cur.execute("SELECT likes FROM BookLikes WHERE bookasin='%s'" %asin)
        data = cur.fetchone()
        return data

    except lite.Error,e:
        print('Error %s: ' %e.args[0])
        sys.exit(1)

    finally:
        if con:
            con.close()

def write_database(asin, nlikes):
    con = None

    try: 
        con = lite.connect('./amazonebooks/Likes.db')
        cur = con.cursor()
        con.execute(
            "INSERT OR REPLACE INTO BookLikes (bookasin,likes)\
            VALUES ('%s','%d')" %(asin, nlikes))
        con.commit()

    except lite.Error,e:
        print('Error %s: ' %e.args[0])
        sys.exit(1)

    finally:
        if con:
            con.close()


@view_config(route_name = 'home', renderer = 'templates/template.pt')
def my_view(request):

# start page view

    form = Form(request, schema=ModelSchema)
    return dict(title='AmazoneBooks',renderer=FormRenderer(form),\
                booklist = [])


@view_config(route_name = 'search',renderer = 'templates/template.pt')
def search_view(request):

# view for search results

    try:

        if request.method == 'POST':
            form = Form(request, schema=ModelSchema)
            booklist = []   # create a book list
            i = 0

            if request.POST['text']:
                books = api.search(Keywords=request.POST['text'],\
                                   SearchIndex='Books')
                for n,book in enumerate(books):
                    booklist.append([])  # adding a list of book properties

                    if hasattr(book.item.ItemAttributes, 'Author'):
                        booklist[i].append(
                            'Author: ' + \
                            removeNonAscii(
                                book.item.ItemAttributes.Author.__str__()))
                    else:
                        booklist[i].append('Author: -')

                    if hasattr(book.item.ItemAttributes, 'Title'):
                        booklist[i].append(
                            'Title: ' + \
                            removeNonAscii(
                                book.item.ItemAttributes.Title.__str__()))
                    else:
                        booklist[i].append('Title: -')

                    if hasattr(book.item.ItemAttributes, 'Publisher'):
                        booklist[i].append(
                            "Publisher: " + \
                            removeNonAscii(
                                book.item.ItemAttributes.Publisher.__str__()))
                    else:
                        booklist[i].append("Publisher: -")

                    if hasattr(book.item, 'SmallImage'):
                        booklist[i].append(
                            removeNonAscii(
                                book.item.SmallImage.URL.__str__()))
                    else:
                        booklist[i].append("-")

                    if hasattr(book.item, 'LargeImage'):
                        booklist[i].append(
                            removeNonAscii(
                                book.item.LargeImage.URL.__str__()))
                    else:
                        booklist[i].append("-")

                    if hasattr(book.item, 'DetailPageURL'):
                        booklist[i].append(
                            removeNonAscii(
                                book.item.DetailPageURL.__str__()))
                    else:
                        booklist[i].append("-")

                    booklist[i].append(removeNonAscii(book.asin))
                    i += 1
                    
            else:
                return dict(title = 'AmazoneBooks',\
                            renderer = FormRenderer(form),booklist = [])
            return dict(title = request.POST['text'],\
                        renderer = FormRenderer(form),booklist = booklist,\
                        css_url = './templates/style.css')
        else:
            pass
    except NoExactMatchesFound:
 	return Response("ERROR. No such item")




@view_config(route_name = 'details',renderer = 'templates/detail.pt')
def details_view(request):

# view for product details

    c = api.lookup(ItemId = request.matchdict['asin'])
    asin = request.matchdict['asin']

    if 'Hello' in request.POST:
        numOfLikes = read_database(asin)

        if numOfLikes == None:
            numOfLikes=(1,)
            write_database(asin,numOfLikes[0])
        else:
            n = numOfLikes[0]
            n += 1
            numOfLikes = (n,)
            write_database(asin,numOfLikes[0])
        resp = Response(body=numOfLikes[0].__str__())
        return resp
    else:
        numOfLikes = read_database(asin)

        if numOfLikes == None:
            write_database(asin,0)
        numOfLikes = read_database(asin)
        iframe = c.item.CustomerReviews.IFrameURL

        if hasattr(c.item, 'MediumImage'):
            mediumImageUrl = c.item.MediumImage.URL

        if hasattr(c.item,'LargeImage'):
            largeImageUrl = c.item.LargeImage.URL

        if hasattr(c.item.ItemAttributes,'Author'):
            author = c.item.ItemAttributes.Author
        else:
            author = 'unknown'

        if hasattr(c.item.ItemAttributes,'Title'):
            title = c.item.ItemAttributes.Title
        else:
            title = 'unknown'

        if hasattr(c.item.ItemAttributes,'NumberOfPages'):
            numOfPages = c.item.ItemAttributes.NumberOfPages
        else:
            numOfPages = 'unknown'

        if hasattr(c.item.ItemAttributes,'Publisher'):
            publisher = c.item.ItemAttributes.Publisher
        else:
            publisher = 'unknown'

        if hasattr(c.item.ItemAttributes,'Languages'):

            if hasattr(c.item.ItemAttributes.Languages,'Language'):
                language = c.item.ItemAttributes.Languages.Language.Name

        if hasattr(c.item.ItemAttributes,'ISBN'):
            isbn = c.item.ItemAttributes.ISBN
        else:
            isbn = 'unknown'

        if hasattr(c.item.ItemAttributes,'PackageDimensions'):
            width = c.item.ItemAttributes.PackageDimensions.Width
            length = c.item.ItemAttributes.PackageDimensions.Length
            height = c.item.ItemAttributes.PackageDimensions.Height
            dim=[width,length,height]
        else:
            dim = ['unknown','unknown','unknown']

        if hasattr(c.item,'SalesRank'):
            salesRank = c.item.SalesRank
        else:
            salesRank = 'unknown'

        if hasattr(c.item.ItemAttributes,'ListPrice'):
            listPrice =  removeNonAscii(
                c.item.ItemAttributes.ListPrice.FormattedPrice.__str__())
            currency = removeNonAscii(
                c.item.ItemAttributes.ListPrice.CurrencyCode.__str__())
            price = [listPrice,currency]
        else:
            price = ['unknown','unknown']

        return dict(mediumImageUrl = mediumImageUrl, \
                    largeImageUrl = largeImageUrl,\
                    title = title, author = author, iframe = iframe, \
                    numOfPages = numOfPages, publisher = publisher,\
                    language = language, isbn = isbn, dim = dim,\
                    salesRank = salesRank, price = price, bookasin = asin, \
                    likes = numOfLikes[0])




