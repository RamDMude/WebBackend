from django.contrib.sites import requests
from django.http import HttpResponse, JsonResponse
import json

def Users(request):

    if request.method == 'GET':

        with open('src/userdb.json','r') as f:
            users = json.load(f)

            return JsonResponse({'status': True, 'users': users})

    elif request.method == 'POST':

        with open('src/userdb.json', 'r') as f:
           users = json.load(f)
        userdata = json.loads(request.body)

        for user in users :
            if user['email'] == userdata['email']:
                return JsonResponse({'status': False, 'message': 'User already exists!'})

        users.append(userdata)

        with open('src/userdb.json', 'w') as f:
            json.dump(users,f,indent=4)

        return JsonResponse({'status': True, 'message':"Account created successfully"})

def login(request):

    with open('src/userdb.json', 'r') as f:
        users = json.load(f)

    userdata = json.loads(request.body)

    a = False
    for user in users:
        if user['email'] == userdata['email'] and user['password'] == userdata['password']:
            a = True
            return JsonResponse({'status': "true", 'name': user['firstname'], 'message': "Login Successful"})
    if a == False :

        return JsonResponse({'status': False, 'message': 'Username or password is incorrect'})


def menswear(request):
    with open('src/menswear.json', 'r') as f:
        mens = json.load(f)

        return JsonResponse({'status': True, 'mens': mens})

def mensproduct(request):

    with open('src/menswear.json', 'r') as f:
        mens = json.load(f)

    productdata = json.loads(request.body)


    for product in mens:
        if (product['name'] == productdata['productname']):

            return JsonResponse({'status': "true",'photo' : product['picture'] ,'stock' : product['stock'] ,'color' : product['color'] ,'sleeve' : product['sleeve'] ,'material' : product['material'] ,'suitable' : product['suitable'] ,'fit' : product['fit']} )

