class ErrorCollection(object):
    def __init__(self, code, status, message):
        self.code = code
        self.status = status
        self.message = message

    # ...

    def as_md(self):
        return (
            '\n\n> **%s**\n\n```\n{\n\n\t"code": "%s"\n\n\t"message": "%s"\n\n}\n\n```'
            % (self.message, self.code, self.message)
        )

