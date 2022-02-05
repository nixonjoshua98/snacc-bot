
class RevoltTable:
    def __init__(self, headers: tuple[str, ...]):
        self.headers = headers
        self.rows = []

    def add_row(self, *row):
        self.rows.append([str(ele) for ele in row])

    def string(self) -> str:
        ls = [
            f"| {' | '.join(self.headers)} |",
            f"{'|:-------' * len(self.headers)}|",
        ]

        ls.extend(f"| {' | '.join(row)} |" for row in self.rows)

        return "\n".join(ls)
