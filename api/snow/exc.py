""" RevealingSnow exception classes """


class RSError(Exception):
    def __init__(self, msg):
        super(RSError, self).__init__()
        self.msg = msg

    def __str__(self):
        return self.msg
