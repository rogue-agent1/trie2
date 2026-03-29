#!/usr/bin/env python3
"""Trie (prefix tree) with autocomplete and pattern matching."""
import sys

class TrieNode:
    __slots__ = ('children','end','count')
    def __init__(self):
        self.children = {}
        self.end = False
        self.count = 0

class Trie:
    def __init__(self):
        self.root = TrieNode()
    def insert(self, word):
        node = self.root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
            node.count += 1
        node.end = True
    def search(self, word):
        node = self._find(word)
        return node is not None and node.end
    def starts_with(self, prefix):
        return self._find(prefix) is not None
    def _find(self, prefix):
        node = self.root
        for ch in prefix:
            if ch not in node.children: return None
            node = node.children[ch]
        return node
    def autocomplete(self, prefix, limit=10):
        node = self._find(prefix)
        if not node: return []
        results = []
        def dfs(n, path):
            if len(results) >= limit: return
            if n.end: results.append(prefix + path)
            for ch in sorted(n.children):
                dfs(n.children[ch], path + ch)
        dfs(node, "")
        return results
    def count_prefix(self, prefix):
        node = self._find(prefix)
        return node.count if node else 0
    def delete(self, word):
        def _del(node, word, i):
            if i == len(word):
                if not node.end: return False
                node.end = False
                return len(node.children) == 0
            ch = word[i]
            if ch not in node.children: return False
            should_del = _del(node.children[ch], word, i+1)
            if should_del:
                del node.children[ch]
                return not node.end and len(node.children) == 0
            node.children[ch].count -= 1
            return False
        _del(self.root, word, 0)

def test():
    t = Trie()
    for w in ["apple","app","application","apt","bat","bath"]:
        t.insert(w)
    assert t.search("app")
    assert not t.search("ap")
    assert t.starts_with("ap")
    ac = t.autocomplete("app")
    assert "apple" in ac and "application" in ac
    assert t.count_prefix("app") == 3
    assert t.count_prefix("bat") == 2
    t.delete("app")
    assert not t.search("app")
    assert t.search("apple")
    print("  trie2: ALL TESTS PASSED")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test": test()
    else: print("Trie with autocomplete")
