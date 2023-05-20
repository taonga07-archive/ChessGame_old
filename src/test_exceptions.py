a= {
    "Errors":{
        "ErrNone": {
            "code": 0,
            "message":"No error"
        },
        "ErrCheckMate": {
            "code": 1,
            "message":"Checkmate"
        },
        "ErrCheck": {
            "code": 2,
            "message":"Check"
        },
        "ErrInvMove": {
            "code": 3,
            "message":"Invalid move"
        },
        "ErrInvColour": {
            "code": 4,
            "message":"Invalid colour"
        },
        "ErrInvCommand": {
            "code": 5,
            "message":"Invalid command"
        },
        "ErrInvCommandMove": {
            "code": 6,
            "message":"Invalid command move"
        }
    },
}

def raise_exception(exception):
    "Raise an exception of the given type specified in the dictionary of errors"
    raise type(exception[0], (Exception,), {"__module__": Exception.__module__, "code": exception[2]})(exception[1])

raise_exception(["ErrInvCommandMove", "Invalid command move", 6])