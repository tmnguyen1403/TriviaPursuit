class Player:
    """Manage Player to communicate with other system about player position
    """    
    def __init__(self, info) -> None:
        self.position = info["position"]
        self.name = info["name"]
        self.token = info["token"]
        self.color = info["color"]
        self.init_short_name()

    def update(self, new_position):
        print(f"player current position: {self.position}")
        print(f"player new position: {new_position}")
        self.position = new_position

    def init_short_name(self):
        if len(self.name) < 2:
             self.short_name = self.name
        else:
            names = self.name.split()
            if len(names) >= 2:
                first_initial = names[0][0]
                last_initial = names[-1][0]
                self.short_name = first_initial+last_initial
            else:
                self.short_name = names[0][0:2]
        self.short_name = self.short_name.upper()

    def get_position(self):
        return self.position
    
    def get_name(self):
        return self.name
    
    def get_short_name(self):
        return self.short_name
    
    def get_color(self):
        return self.color