# Project 1: Simple Key-Value Store
# Name: Likitha
# EUID: 11682461

import sys, os

DATA_FILE = "data.db"     # append-only log file
NULL_VALUE = "NULL"       # what to print for missing keys


# ---------------- In-Memory Index ----------------
class KVIndex:
    def __init__(self):
        # list of [key, value] pairs (NOT a dict)
        self.pairs = []

    def _find_index(self, key):
        # search from the end so last write wins
        for i in range(len(self.pairs) - 1, -1, -1):
            if self.pairs[i][0] == key:
                return i
        return -1

    def set(self, key, value):
        idx = self._find_index(key)
        if idx >= 0:
            self.pairs[idx][1] = value
        else:
            self.pairs.append([key, value])

    def get(self, key):
        idx = self._find_index(key)
        if idx >= 0:
            return self.pairs[idx][1]
        return None


# ---------------- Store with Persistence ----------------
class KVStore:
    def __init__(self, filename=DATA_FILE):
        self.filename = filename
        self.index = KVIndex()
        self._replay()

    def _replay(self):
        """Rebuild the in-memory index by reading data.db"""
        if not os.path.exists(self.filename):
            return
        with open(self.filename, "r", encoding="utf-8") as f:
            for line in f:
                line = line.rstrip("\n")
                if not line or not line.startswith("SET "):
                    continue
                # line format: SET <key> <value>
                parts = line.split(" ", 2)
                if len(parts) == 3:
                    _, key, value = parts
                    self.index.set(key, value)

    def set(self, key, value):
        """Append to log file and update memory"""
        with open(self.filename, "a", encoding="utf-8") as f:
            f.write(f"SET {key} {value}\n")
            f.flush()
            os.fsync(f.fileno())  # force write to disk
        self.index.set(key, value)

    def get(self, key):
        return self.index.get(key)


# ---------------- Command-Line Interface ----------------
def main():
    store = KVStore()

    for raw in sys.stdin:
        line = raw.strip()
        if not line:
            continue

        if line == "EXIT":
            return

        if line.startswith("SET "):
            parts = line.split(" ", 2)
            if len(parts) == 3:
                _, key, value = parts
                store.set(key, value)
            # ignore malformed SET
            continue

        if line.startswith("GET "):
            parts = line.split(" ", 1)
            if len(parts) == 2:
                _, key = parts
                val = store.get(key)
                # IMPORTANT: flush so Gradebot sees output
                print(val if val is not None else NULL_VALUE, flush=True)
            else:
                print(NULL_VALUE, flush=True)
            continue

        # ignore any other input

if __name__ == "__main__":
    main()

