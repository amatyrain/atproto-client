class BlueskyClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client = None
