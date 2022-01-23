class A():
    att = 0
    def __init__(self) -> None:
        pass

    @classmethod
    def change_att(cls, val):
        cls.att = val

b = A()
c = A()
A.change_att(2)

print(b.att, c.att)