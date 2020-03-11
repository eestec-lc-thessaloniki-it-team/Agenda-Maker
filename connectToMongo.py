from pymongo import MongoClient
from datetime import date

# fill this with your personal
username="root"
passwrod="rootPass"
database="lcThessaloniki"

url="""mongodb://{}:{}@127.0.0.1/{}""".format(username,passwrod,database)
client=MongoClient(url,authSource="admin")['lcThessaloniki']

data={
    'lc': 'thessaloniki',
    'date': date.today().strftime("%d/%m/%Y"),
    'agenda':[ # this will be a list of objects  but for now lets assume that there are title, subtitle
        {
            'title':'this is the first topic',
            'subtitle':'this is its subtitle1'
        },
        {
            'title':'this is the second topic',
            'subtitle':'this is its subtitle2'
        }
    ]
}

db=client.lcThessaloniki #will create a database named lcThessaloniki
result=db.agendas.insert_one(data) # will create a collection named agenas in the database lcThessaloniki and insert the data
print(result.inserted_id)

# lets retrieve to see if we got them
lcThessaloniki=db.agendas.find_one({'lc':'thessaloniki'})
print(lcThessaloniki)
