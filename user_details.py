class UserDetails:
    def __init__(self, ip, message):
        self.ipAddress = ip
        self.message = message

    def to_json(self):
        return "{{\"ipAddress\": {}, \"message\": {}}}".format(self.ipAddress, self.message)
