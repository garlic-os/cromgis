import random
import sys
import dataset
from typing import Any, AnyStr, ItemsView, Iterable

root_dir = sys.path[0]


def chunks(l, n) -> Iterable:
    """Splits a sequence into a iter of lists with size n"""
    for i in range(0, len(l), n):
        yield l[i:i+n]


def weighted_random(pairs: ItemsView) -> Any:
    """a"""
    total = sum(pair[0] for pair in pairs)
    r = random.randint(1, total)
    for weight, value in pairs:
        r -= weight
        if r <= 0:
            return value


class AwfulMarkov:

    def __init__(self, table_name: AnyStr, *, corpus: AnyStr = None, state_size: int = None) -> None:
        """
Initializes a Markov model.
Since data is stored in a database, a table name to reference must always be used when initializing the object.
Providing the corpus param will ALWAYS train further.
To draw data from previous generation, leave the "corpus" param alone.
If you still want to be able to train iteratively, specify a state size that matches that of your original trained data.
        """
        self._d = dataset.connect(f"sqlite:///{root_dir}/data.db")
        self._tn = table_name  # shortcut
        self._table = self._d[table_name]
        self._state = state_size or 3

        if corpus:
            cleaned = corpus.replace("  ", "")
            self._train_all(cleaned)

    def _train_all(self, collection: AnyStr) -> None:
        """Take a bunch of text, split it, and train."""
        c = collection.split("\n")
        for i, line in enumerate(c):
            chunked = chunks(line.split(" "), self._state)
            filtered = filter(lambda k: len(k) == self._state, chunked)
            mapped = list(map(lambda k: " ".join(k), filtered))
            if len(mapped) >= 2:
                for first, second in zip(mapped, mapped[1:]):
                    self._train_from_pair(first, second)

            # print(f"Completed step {i + 1} / {len(c)}")

    def _train_from_pair(self, first: AnyStr, second: AnyStr) -> None:
        r = self._table.find_one(first=first, second=second)
        if r:
            del r["id"]
            r["weight"] += 1
            self._table.upsert(r, ["first", "second"])
        else:
            self._table.insert({"first": str(first), "second": str(second), "weight": 1})

    def generate(self) -> str:
        item = list(self._d.query(f"SELECT * FROM {self._tn} ORDER BY RANDOM() LIMIT 1;"))[0]
        s = item["first"]
        for i in range(random.randint(3, 35)):  # allow config of this later
            res = self._table.find(first=item["second"])
            items = [[r["weight"], dict(r)] for r in res]
            try:
                item = weighted_random(items)
                s = f"{s} {item['first']}"
            except Exception:  # TODO: stop catching such a wide exception
                break  # ran out of words to follow

        return s


if __name__ == "__main__":
    a = AwfulMarkov("markov_ooer", state_size=2)  # enough for previous data + new (iter) training
    while True:
        input(a.generate())
