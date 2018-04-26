class Person:
    def __init__(self,value = 'Wu zhenkang'):
        self.name = value
    def setName(self,name):
        self.name = name
    def getName():
        return self.name
    def greet(self):
        print("Hello, world!I'm %s." %self.name)


class Bird:
    def __init__(self):
        self.hungry = True
    def eat(self):
        if self.hungry:
            print("Assah...")
            self.hungry = False
        else:
            print("No,thanks;")

class SongBird(Bird):
    def __init__(self):
        Bird.__init__(self) #super(SongBird,self).__init__() 
        self.sound = 'Squaw!'
    def sing(self):
        print (self.sound)
