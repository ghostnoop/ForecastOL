class B:
    def __init__(self):
        self.w = None


class A:
    def __init__(self):
        self.t = B()


print(A().t.w.id if A().t.w is not None else 1)
