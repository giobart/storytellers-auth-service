from auth.extensions import jwt
from auth.utility import errors


@jwt.unauthorized_loader
def unauthorized_loader(reason):
    return errors.response('501')


@jwt.revoked_token_loader
def revoked_loader():
    return errors.response('502')


@jwt.needs_fresh_token_loader
def fresh_loader():
    return errors.response('503')


@jwt.expired_token_loader
def expired_loader():
    return errors.response('504')


@jwt.invalid_token_loader
def invalid_loader():
    return errors.response('505')
