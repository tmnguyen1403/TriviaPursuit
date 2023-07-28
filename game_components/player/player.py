class Player:
    """Manage Player to communicate with other system about player position
    """    
    def __init__(self, info) -> None:
        self.test = 0
        self.position = info["position"]
        self.name = info["name"]
        self.token = info["token"]
        self.score = []
        self.color = info["color"]
    def move(self):
        return 0
    def update(self, new_position):
        print(f"player current position: {self.position}")
        print(f"player new position: {new_position}")
        self.position = new_position
    def get_position(self):
        return self.position
    def get_name(self):
        return self.name
    def get_color(self):
        return self.color