class UserDetails:
    def __init__(self, ip, message):
        self.ip = ip
        self.message = message

    def to_json(self):
        return {"ipAddress": self.ip, "message": self.message}
