from trie2 import Trie
t = Trie()
words = ["apple", "app", "application", "banana", "band", "bandana"]
for w in words: t.insert(w, len(w))
assert len(t) == 6
assert "apple" in t
assert "ap" not in t
assert t.search("apple") == 5
assert t.search("ap") is None
prefix = t.starts_with("app")
assert len(prefix) == 3
assert all(w.startswith("app") for w, _ in prefix)
t.delete("app")
assert "app" not in t
assert "apple" in t
assert len(t) == 5
print("trie2 tests passed")
