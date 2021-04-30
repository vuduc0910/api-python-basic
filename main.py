import bottle
import re
import json
from bottle import get, post, delete, put, request, response

# import models.database as db
import models.db2 as db
app = application = bottle.default_app()
name_pattern = re.compile(r'^[a-zA-Z\d]{1,29}$')
password_pattern = re.compile(r'[A-Za-z0-9@#$%^&+=]{8,16}')
email_pattern = re.compile(r'^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$')


@get('/all')
def get_all():
    """ GET ALL """
    response.headers['Content-Type'] = 'application/json'
    response.status = 200
    users = db.create_query_get()
    return {
        'data': json.dumps(users),
        'status': response.status
    }


@get('/get-one')
def get_one():
    """ GET ONE """
    try:
        if request.query.name is None:
            raise ValueError
        name = request.query.name
        users = db.create_query_get_one(name)
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
def add_user():
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
            if name_pattern.match(data['name']) is None or password_pattern\
                    .fullmatch(data['password']) is None or \
                    email_pattern.fullmatch(data['email']) is None:
                raise ValueError
            name = data['name']
            email = data['email']
            password = data['password']
            users = db.create_query_get()
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
    db.create_query_insert(name, password, email)

    # return 200 Success
    response.headers['Content-Type'] = 'application/json'
    return {
        'data': json.dumps(db.create_query_get()),
        'status': response.status
    }


@put('/update-user')
def update_user():
    """ PUT """
    try:
        users = db.create_query_get()
        if request.query.name is None:
            raise ValueError
        if request.query.name not in [user['name'] for user in users]:
            raise KeyError
        try:
            data = request.json
        except:
            raise ValueError
        if data['name'] is not None and request.query.name != data['name']:
            raise ValueError
        name = data['name']
        new_email = None
        new_pass = None
        if data['email'] is not None or email_pattern \
                .fullmatch(data['email']) is not None:
            new_email = data['email']
        if data['password'] is not None or password_pattern \
                .fullmatch(data['password'] is not None):
            new_pass = data['password']
        user = db.create_query_get_one(name)
        if new_email is None:
            new_email = user['email']
        if new_pass is None:
            new_pass = user['newPass']
        db.create_query_update(name, new_pass, new_email)
    except ValueError:
        response.status = 400
        return {'errors': response.status}
    except KeyError:
        response.status = 409
        return {'errors': response.status}
    response.headers['Content-Type'] = 'application/json'
    return {
        'data': json.dumps(db.create_query_get()),
        'status': response.status
    }


@delete('/delete-user')
def delete_user():
    """ DELETE """
    try:
        if request.query.name is None:
            raise KeyError
        db.create_query_delete(request.query.name)
        response.status = 200
        return {
            'data': json.dumps(db.create_query_get()),
            'status': response.status
        }
    except KeyError:
        response.status = 409
        return {'errors': response.status}


if __name__ == '__main__':
    bottle.run(host='127.0.0.1', port=8000)
