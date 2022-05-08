from flask import jsonify


def Success(data=None):
    return jsonify(msg="success", status=200, data=data)


def ParamsError(data=None):
    return jsonify(msg="params error", status=403, data=data)


def SQLError(data=None):
    return jsonify(msg="SQL error", status=402, data=data)


def PwdError(data=None):
    return jsonify(msg="pwd error", status=401, data=data)


def MessageFailed(data=None):
    return jsonify(msg='failed to', status=400, data=data)
