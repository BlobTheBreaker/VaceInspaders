class A():
    att = 1

    def __init__(self) -> None:
        self.msg = 'hello'

    @classmethod
    def change_att(cls, val):
        cls.att = val


b = A()
c = A()

A.change_att(2)

print(b.att)
print(c.att)