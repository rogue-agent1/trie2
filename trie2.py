#!/usr/bin/env python3
"""Trie (prefix tree) data structure. Zero dependencies."""
import sys

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False
        self.value = None
        self.count = 0

class Trie:
    def __init__(self):
        self.root = TrieNode()
        self.size = 0

    def insert(self, key, value=None):
        node = self.root
        for ch in key:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
            node.count += 1
        if not node.is_end:
            self.size += 1
        node.is_end = True
        node.value = value

    def search(self, key):
        node = self._find(key)
        return node.value if node and node.is_end else None

    def _find(self, prefix):
        node = self.root
        for ch in prefix:
            if ch not in node.children: return None
            node = node.children[ch]
        return node

    def starts_with(self, prefix):
        node = self._find(prefix)
        if not node: return []
        results = []
        self._collect(node, prefix, results)
        return results

    def _collect(self, node, prefix, results):
        if node.is_end:
            results.append((prefix, node.value))
        for ch in sorted(node.children):
            self._collect(node.children[ch], prefix + ch, results)

    def delete(self, key):
        def _del(node, key, depth):
            if depth == len(key):
                if not node.is_end: return False
                node.is_end = False
                self.size -= 1
                return len(node.children) == 0
            ch = key[depth]
            if ch not in node.children: return False
            should_delete = _del(node.children[ch], key, depth + 1)
            if should_delete:
                del node.children[ch]
                return not node.is_end and len(node.children) == 0
            node.children[ch].count -= 1
            return False
        _del(self.root, key, 0)

    def __len__(self): return self.size
    def __contains__(self, key):
        node = self._find(key)
        return node is not None and node.is_end

if __name__ == "__main__":
    t = Trie()
    for w in sys.argv[1:]: t.insert(w)
    print(f"Trie with {len(t)} words")
