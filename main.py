import bottle
from bottle import get,post,delete,put,request,response
import re,json
users = [{'name':'vuduc','password':'123123123','email':'vuduc1711@gmail.com'}]
app = application = bottle.default_app()
name_pattern = re.compile(r'^[a-zA-Z\d]{1,64}$')
password_pattern = re.compile(r'[A-Za-z0-9@#$%^&+=]{8,}')
email_pattern = re.compile(r'^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$')

# GET
@get('/all')
def getAll():
    response.headers['Content-Type'] = 'application/json'
    return json.dumps(users)
@get('/get-one')
def getOne():
    try:
        if request.query.name is None:
            raise ValueError
        if  request.query.name not in [user['name'] for user in users] :
            raise KeyError
        name = request.query.name
        response.headers['Content-Type'] = 'application/json'
        return json.dumps([user for user in users if user['name'] == name])
    except ValueError:
        response.status = 400
        return
    except KeyError:
        response.status = 409
        return


#POST
@post('/add-user')
def addUser():
    try:
        # parse input data
        try:
            data = request.json
        except:
            raise ValueError
        if data is None:
            raise ValueError
        # extract and validate name
        try:
            if name_pattern.match(data['name']) is None or password_pattern.fullmatch(data['password']) is None or \
                    email_pattern.fullmatch(data['email']) is None:
                raise ValueError
            name = data['name']
            email = data['email']
            password = data['password']
        except (TypeError, KeyError):
            raise ValueError

        # check for existence
        if name in [user['name'] for user in users]:
            raise KeyError

    except ValueError:
        # if bad request data, return 400 Bad Request
        response.status = 400
        return

    except KeyError:
        # if name already exists, return 409 Conflict
        response.status = 409
        return

    # add user
    users.append({'name': name ,'password' : password, 'email': email})

    # return 200 Success
    response.headers['Content-Type'] = 'application/json'
    return json.dumps(users)

#PUT
@put('/update-user')
def updateUser():
    try:
        if request.query.name is None:
            raise ValueError
        if request.query.name not in [user['name'] for user in users]:
            raise KeyError
        try:
            data = request.json
        except:
            raise ValueError
        if data['name'] is not None and request.query.name != data['name'] :
            raise ValueError
        name = data['name']
        newEmail = None
        newPass = None
        if data['email'] is not None or email_pattern.fullmatch(data['email']) is not None:
            newEmail = data['email']
        if data['password'] is not None or password_pattern.fullmatch(data['password'] is not None):
            newPass = data['password']
        for user in users:
            if user['name'] == name:
                if newEmail is not None:
                    user['email'] =newEmail
                if newPass is not None:
                    user['password'] = newPass
    except ValueError:
        response.status = 400
        return
    except KeyError:
        response.status = 409
        return
    response.headers['Content-Type'] = 'application/json'
    return json.dumps(users)
if __name__ == '__main__':
    bottle.run(host = '127.0.0.1', port = 8000)
