from target.target import Target


class Enemy(Target):

    def __init__(self, core) -> None:
        super().__init__(core, is_enemy=True, is_gadget=False)

