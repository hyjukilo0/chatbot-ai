

class Order:
    def __init__(self):
        self.productname = None
        self.color = None
        self.material = None
        self.materialadv = None
        self.cost = None
        self.amount = None
        
        self.size = None
        self.height = None
        self.weight = None
        
        self.customername = None
        self.address = None
        self.phone = None

    def setproduct(self, name, color, material, materialadv, cost):
        self.productname = name
        self.color = color
        self.material = material
        self.materialadv = materialadv
        self.cost = cost
    def setamount(self, x):
        self.amount = x
    def setsize(self, x):
        self.size = x
    def setheight(self, x):
        self.height = x
    def setweight(self, x):
        self.weight = x
    
    def setcustomername(self, x):
        self.customername = x
    def setaddress(self, x):
        self.address = x
    def setphone(self, x):
        self.phone = x

    def checkfullinfo(self):
        if self.productname == None:
            return "productname"
        elif self.color == None:
            return "color"
        elif self.size == None:
            return "size"
        elif self.amount == None:
            return "amount"
        # elif self.customername == None:
        #     return "customername"
        elif self.address == None:
            return "address"
        elif self.phone == None:
            return "phone"
        else:
            return "full"
