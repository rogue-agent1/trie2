#!/usr/bin/env python3
"""trie2 - Trie with prefix search, autocomplete, and wildcard matching."""
import sys

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False
        self.count = 0

class Trie:
    def __init__(self):
        self.root = TrieNode()
        self.size = 0

    def insert(self, word):
        node = self.root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
            node.count += 1
        if not node.is_end:
            self.size += 1
        node.is_end = True

    def search(self, word):
        node = self._find(word)
        return node is not None and node.is_end

    def starts_with(self, prefix):
        return self._find(prefix) is not None

    def _find(self, prefix):
        node = self.root
        for ch in prefix:
            if ch not in node.children:
                return None
            node = node.children[ch]
        return node

    def autocomplete(self, prefix, limit=10):
        node = self._find(prefix)
        if not node:
            return []
        results = []
        def dfs(n, path):
            if len(results) >= limit:
                return
            if n.is_end:
                results.append(prefix + path)
            for ch in sorted(n.children):
                dfs(n.children[ch], path + ch)
        dfs(node, "")
        return results

    def count_prefix(self, prefix):
        node = self._find(prefix)
        return node.count if node else 0

    def wildcard_search(self, pattern):
        results = []
        def dfs(node, i, path):
            if i == len(pattern):
                if node.is_end:
                    results.append(path)
                return
            if pattern[i] == ".":
                for ch, child in node.children.items():
                    dfs(child, i + 1, path + ch)
            elif pattern[i] in node.children:
                dfs(node.children[pattern[i]], i + 1, path + pattern[i])
        dfs(self.root, 0, "")
        return results

def test():
    t = Trie()
    for w in ["apple", "app", "application", "banana", "band", "ban"]:
        t.insert(w)
    assert t.size == 6
    assert t.search("apple")
    assert t.search("app")
    assert not t.search("ap")
    assert t.starts_with("ap")
    assert not t.starts_with("xyz")
    ac = t.autocomplete("app")
    assert "app" in ac and "apple" in ac and "application" in ac
    assert t.count_prefix("app") == 3
    assert t.count_prefix("ban") == 3
    wc = t.wildcard_search("b.n")
    assert "ban" in wc
    wc2 = t.wildcard_search("app.e")
    assert "apple" in wc2
    print("All tests passed!")

if __name__ == "__main__":
    test() if "--test" in sys.argv else print("trie2: Trie with autocomplete. Use --test")
