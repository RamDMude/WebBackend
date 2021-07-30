from django.contrib.sites import requests
import pymongo
from bson import ObjectId
from django.http import HttpResponse, JsonResponse
import json
from django.conf import settings
import jwt
import datetime
from passlib.apps import custom_app_context as pwd_context
from rest_framework.decorators import api_view

from Webback import utility



client = pymongo.MongoClient("mongodb://localhost:27017/")
ecomm = client["ecom"]
usersclc = ecomm["userdb"]
menswear1 = ecomm["menswear"]
womenswear1 = ecomm["womenswear"]
watches1 = ecomm["watches"]


def idconvertor() :
    users1 = [i for i in usersclc.find()]
    for user in users1:
        user['_id'] = str(user['_id'])
    return users1

def idconvertormen() :
    mens = [j for j in menswear1.find()]
    for men in mens:
        men['_id'] = str(men['_id'])
    return mens

def idconvertorwomen() :
    womens = [i for i in womenswear1.find()]
    for women in womens:
        women['_id'] = str(women['_id'])
    return womens

def idconvertorwatches() :
    watches = [i for i in watches1.find()]
    for watch in watches:
        watch['_id'] = str(watch['_id'])
    return watches

def Users(request):

    if request.method == 'GET':

        # with open('src/userdb.json', 'r') as f:
        #    users = json.load(f)

        users1 = idconvertor()

        return JsonResponse({'status': True, 'users': users1})

    elif request.method == 'POST':

        users1 = idconvertor()
        userdata = json.loads(request.body)

        for user in users1 :
            if user['email'] == userdata['email']:
                return JsonResponse({'status': False, 'message': 'User already exists!'})

        userdata['password'] = pwd_context.hash(userdata['password'])

        userdata["cartprod"] = []
        userdata["orderprod"] = []
        usersclc.insert(userdata)


        # with open('src/userdb.json', 'w') as f:
        #     json.dump(users,f,indent=4)

        return JsonResponse({'status': True, 'message':"Account created successfully"})


def login(request):

    users1 = idconvertor()
    userdata = json.loads(request.body)

    a = False
    for user in users1:

        if user['email'] == userdata['email'] and pwd_context.verify(userdata['password'] ,user['password']):
            a = True
            # create a token
            token = jwt.encode(
                {'email': user['email'],
                 'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=24 * 60 * 60)
                 },
                settings.SECRET_KEY,
                algorithm="HS256").decode('utf-8')
            return JsonResponse({'status': "true", 'name': user['firstname'], 'message': "Login Successful", 'token': token})
    if a == False :

        return JsonResponse({'status': False, 'message': 'Username or password is incorrect'})

# def showdetails
def fetchdetails(request):
    users1 = idconvertor()
    req = json.loads(request.body)

    for user in users1:
        if user['email'] == req['email']:
            return JsonResponse({'status':True, 'firstname':user['firstname'],'lastname':user['lastname'],'number':user['number']})

def changedetails(request):
    users1 = idconvertor()
    req = json.loads(request.body)

    for user in users1:
        if user['email'] == req['email']:
            usersclc.update_one({'email': req['email']}, {'$set': {"firstname": req["firstname"]}})
            usersclc.update_one({'email': req['email']}, {'$set': {"lastname": req["lastname"]}})
            usersclc.update_one({'email': req['email']}, {'$set': {"number": req["number"]}})
            return JsonResponse({'status': "True"})

def menswear(request):
    # with open('src/menswear.json', 'r') as f:
    #     mens = json.load(f)

    mens = idconvertormen()

    return JsonResponse({'status': True, 'mens': mens})

def mensproduct(request):

    mens = idconvertormen()
    productdata = json.loads(request.body)


    for product in mens:
        if (product['_id'] == productdata['productid']):

            return JsonResponse({'status': "true",'_id':product['_id'],'name': product['name'],'photo' : product['picture'] ,'price' : product['price'],'oldp' : product['oldprice'] ,'stock' : product['stock'] ,'color' : product['color'] ,'sleeve' : product['sleeve'] ,'material' : product['material'] ,'suitable' : product['suitable'] ,'fit' : product['fit']} )


def womenswear(request):
    # with open('src/menswear.json', 'r') as f:
    #     mens = json.load(f)

    womens = idconvertorwomen()

    return JsonResponse({'status': True, 'womens': womens})

def womensproduct(request):

    womens = idconvertorwomen()
    productdata = json.loads(request.body)


    for product in womens:
        if (product['_id'] == productdata['productid']):

            return JsonResponse({'status': "true",'_id':product['_id'],'name': product['name'],'photo' : product['picture'] ,'price' : product['price'],'oldp' : product['oldprice'] ,'stock' : product['stock'] ,'color' : product['color'] ,'sleeve' : product['sleeve'] ,'material' : product['material'] ,'suitable' : product['suitable'] ,'fit' : product['fit']} )

def watches(request):
    # with open('src/menswear.json', 'r') as f:
    #     mens = json.load(f)

    watches = idconvertorwatches()

    return JsonResponse({'status': True, 'watches': watches})

def watchesproduct(request):

    watches = idconvertorwatches()
    productdata = json.loads(request.body)


    for product in watches:
        if (product['_id'] == productdata['productid']):

            return JsonResponse({'status': "true",'_id':product['_id'],'name': product['name'],'photo' : product['picture'] ,'price' : product['price'] ,'oldp' : product['oldprice'],'stock' : product['stock'] ,'color' : product['color'] ,'sleeve' : product['sleeve'] ,'material' : product['material'] ,'suitable' : product['suitable'] ,'fit' : product['fit']} )

# @utility.requireLogin
# @api_view(['POST'])
def showcart(request):

    users1 = idconvertor()
    req = json.loads(request.body)

    for user in users1:
        if user['email'] == req['email']:

            return JsonResponse({'status':"True" , 'cartprods':user['cartprod']})

# @utility.requireLogin
def addtocart(request):

    users1 = idconvertor()
    req = json.loads(request.body)

    for user in users1:
        if user['email'] == req['email']:
            usersclc.update_one({'email': req['email']}, {'$push': {'cartprod': req['productid']}})
            return JsonResponse({'status': "True"})

# @utility.requireLogin
def removefromcart(request):

    users1 = idconvertor()
    req = json.loads(request.body)

    for user in users1:
        if user['email'] == req['email']:
            usersclc.update_one({'email': req['email']}, {'$pull': {'cartprod': req['productid']}})
            return JsonResponse({'status': "True"})

def orderfunc(request):

    users1 = idconvertor()
    req = json.loads(request.body)

    for user in users1:
        if user['email'] == req['email']:
            productwid = [i for i in usersclc.find({'email': req['email']})]
            for prod in productwid[0]["cartprod"]:
                usersclc.update_one({'email': req['email']}, {'$push': {'orderprod': prod}})
                usersclc.update_one({'email': req['email']}, {'$pull': {'cartprod': prod}})


def showorders(request):

    users1 = idconvertor()
    req = json.loads(request.body)

    for user in users1:
        if user['email'] == req['email']:

            return JsonResponse({'status':"True" , 'orderprod':user['orderprod']})
