class RegisterError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        print(self.msg)


class TokenValidError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        print(self.msg)


class LoginPureError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        print(self.msg)


class WechatGrandError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        print(self.msg)
