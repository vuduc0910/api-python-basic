import bottle,re,json
from bottle import get,post,delete,put,request,response

import models.database as db

app = application = bottle.default_app()
name_pattern = re.compile(r'^[a-zA-Z\d]{1,29}$')
password_pattern = re.compile(r'[A-Za-z0-9@#$%^&+=]{8,16}')
email_pattern = re.compile(r'^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$')


@get('/all')
def getAll():
    """ GET ALL """
    response.headers['Content-Type'] = 'application/json'
    response.status = 200
    users = db.create_query_get("1' or 1 = 1 --")
    return {
        'data': json.dumps(users),
        'status': response.status
    }


@get('/get-one')
def getOne():
    """ GET ONE """
    try:
        if request.query.name is None:
            raise ValueError
        name = request.query.name
        users = db.create_query_get(name)
        if users == []:
            raise KeyError
        response.headers['Content-Type'] = 'application/json'
        response.status = 200
        return {
            'data': json.dumps(users),
            'status': response.status
        }
    except ValueError:
        response.status = 400
        return {'errors': response.status}
    except KeyError:
        response.status = 409
        return {'errors': response.status}


@post('/add-user')
def addUser():
    """ POST """
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
            users = db.create_query_get("1' or 1 = 1 --")
        except (TypeError, KeyError):
            raise ValueError

        # check for existence
        if name in [user['name'] for user in users]:
            raise KeyError

    except ValueError:
        # if bad request data, return 400 Bad Request
        response.status = 400
        return {'errors': response.status}

    except KeyError:
        # if name already exists, return 409 Conflict
        response.status = 409
        return {'errors': response.status}

    # add user
    db.create_query_insert(name,password,email)

    # return 200 Success
    response.headers['Content-Type'] = 'application/json'
    return {
        'data': json.dumps(db.create_query_get("1' or 1 = 1 --")),
        'status': response.status
    }


@put('/update-user')
def updateUser():
    """ PUT """
    try:
        users = db.create_query_get("1' or 1 = 1 --")
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
        user = db.create_query_get(name)
        if newEmail is None:
            newEmail = user['email']
        if newPass is None:
            newPass = user['newPass']
        db.create_query_update(name, newPass, newEmail)
    except ValueError:
        response.status = 400
        return {'errors': response.status}
    except KeyError:
        response.status = 409
        return {'errors': response.status}
    response.headers['Content-Type'] = 'application/json'
    return {
        'data': json.dumps(db.create_query_get("1' or 1 = 1 --")),
        'status': response.status
    }


@delete('/delete-user')
def deleteUser():
    """ DELETE """
    try:
        users = db.create_query_get("1' or 1 = 1 --")
        if request.query.name is None:
            raise KeyError
        db.create_query_delete(request.query.name)
        response.status = 200
        return {
            'data' : json.dumps(db.create_query_get("1' or 1 = 1 --")),
            'status' : response.status
        }
    except KeyError:
        response.status = 409
        return {'errors': response.status}


if __name__ == '__main__':
    bottle.run(host = '127.0.0.1', port = 8000)
