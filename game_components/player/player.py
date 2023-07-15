class Player:
    """Manage Player to communicate with other system about player position
    """    
    def __init__(self, info) -> None:
        self.test = 0
        self.position = info["position"]
        self.name = info["name"]
        self.token = info["token"]
        self.score = []
    def move(self):
        return 0
    def update(self, new_position):
        self.position = new_position