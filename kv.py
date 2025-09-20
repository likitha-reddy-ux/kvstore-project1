#!/usr/bin/env python3
"""
Simple Key-Value Store Project

Commands:
  SET <key> <value>   -> store a value under a key
  GET <key>           -> retrieve the value if it exists
  EXIT                -> quit the program

Features:
- Every SET is saved into a file named data.db (append-only log).
- When program starts, it replays data.db to rebuild memory.
- Uses a custom list of pairs [key, value] (NOT Python dict).
"""

import sys, os

DATA_FILE = "data.db"     # file where data will be saved
NULL_VALUE = "NULL"       # what to print when key not found


# ---------------- In-Memory Index ----------------
class KVIndex:
    def __init__(self):
        # we use a list of [key, value] pairs instead of dict
        self.pairs = []

    def _find_index(self, key):
        # search backwards so we always find the most recent write
        for i in range(len(self.pairs) - 1, -1, -1):
            if self.pairs[i][0] == key:
                return i
        return -1

    def set(self, key, value):
        """Store or overwrite a key with a value in memory"""
        idx = self._find_index(key)
        if idx >= 0:
            self.pairs[idx][1] = value
        else:
            self.pairs.append([key, value])

    def get(self, key):
        """Return value for key, or None if not found"""
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
                line = line.strip()
                if not line:
                    continue
                if line.startswith("SET "):
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
        """Get value from memory"""
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
            # silently ignore malformed SET

        elif line.startswith("GET "):
            parts = line.split(" ", 1)
            if len(parts) == 2:
                _, key = parts
                val = store.get(key)
                print(val if val is not None else NULL_VALUE)
            else:
                print(NULL_VALUE)
        # ignore any other commands


if __name__ == "__main__":
    main()
