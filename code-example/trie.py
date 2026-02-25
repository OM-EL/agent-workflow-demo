"""
Trie (Prefix Tree) — compact implementation with path compression.

Techniques used:
  - Path compression: collapses single-child chains into one node to save
    space and speed up lookups on long shared prefixes.
  - Iterative traversal: all public methods avoid recursion so the call
    stack stays constant regardless of key length.
  - Generator-based enumeration: `keys_with_prefix` and `__iter__` yield
    results lazily via an explicit stack, keeping memory usage low even
    when the trie holds millions of entries.

Complexity (n = key length, m = number of matches):
  insert / search / delete   — O(n)
  starts_with                 — O(n)
  keys_with_prefix            — O(n + m)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterator


@dataclass
class _TrieNode:
    """Internal node of the compressed trie."""

    children: dict[str, _TrieNode] = field(default_factory=dict)
    is_end: bool = False
    value: Any = None
    # For path compression: a node can store a full fragment instead of a
    # single character.  The edge label from parent to child is the fragment.
    fragment: str = ""


class Trie:
    """A compressed prefix tree that maps string keys to arbitrary values.

    >>> t = Trie()
    >>> t.insert("apple", 1)
    >>> t.insert("app", 2)
    >>> t.insert("application", 3)
    >>> t.search("app")
    2
    >>> t.search("apple")
    1
    >>> t.starts_with("app")
    True
    >>> sorted(t.keys_with_prefix("app"))
    ['app', 'apple', 'application']
    """

    def __init__(self) -> None:
        self._root = _TrieNode()
        self._size = 0

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def insert(self, key: str, value: Any = True) -> None:
        """Insert *key* with an optional *value* (default ``True``)."""
        node = self._root
        i = 0
        while i < len(key):
            char = key[i]
            if char not in node.children:
                # No matching child — create a leaf with the remaining suffix.
                leaf = _TrieNode(fragment=key[i:], is_end=True, value=value)
                node.children[char] = leaf
                self._size += 1
                return
            child = node.children[char]
            fragment = child.fragment
            # Walk along the shared prefix of the remaining key and
            # the child's fragment.
            j = 0
            while j < len(fragment) and i + j < len(key) and key[i + j] == fragment[j]:
                j += 1
            if j == len(fragment):
                # The entire fragment matched — descend into the child.
                node = child
                i += j
            else:
                # Partial match — split the existing node.
                split = _TrieNode(fragment=fragment[:j])
                split.children[fragment[j]] = child
                child.fragment = fragment[j:]
                node.children[char] = split
                if i + j == len(key):
                    split.is_end = True
                    split.value = value
                    self._size += 1
                    return
                remaining = key[i + j :]
                new_leaf = _TrieNode(
                    fragment=remaining, is_end=True, value=value
                )
                split.children[remaining[0]] = new_leaf
                self._size += 1
                return
        # Exhausted key — mark current node as end.
        if not node.is_end:
            self._size += 1
        node.is_end = True
        node.value = value

    def search(self, key: str) -> Any | None:
        """Return the value for *key*, or ``None`` if absent."""
        node = self._find_node(key)
        if node is not None and node.is_end:
            return node.value
        return None

    def starts_with(self, prefix: str) -> bool:
        """Return ``True`` if any key starts with *prefix*."""
        return self._find_node(prefix) is not None

    def delete(self, key: str) -> bool:
        """Remove *key* from the trie. Returns ``True`` if it existed."""
        # Iterative delete with parent tracking.
        path: list[tuple[_TrieNode, str]] = []
        node = self._root
        i = 0
        while i < len(key):
            char = key[i]
            if char not in node.children:
                return False
            child = node.children[char]
            fragment = child.fragment
            if not key[i:].startswith(fragment):
                return False
            path.append((node, char))
            node = child
            i += len(fragment)
        if not node.is_end:
            return False
        node.is_end = False
        node.value = None
        self._size -= 1
        # Clean up childless, non-terminal nodes bottom-up.
        while path and not node.children and not node.is_end:
            parent, edge_char = path.pop()
            del parent.children[edge_char]
            node = parent
        # Re-merge single-child internal nodes after deletion.
        if len(node.children) == 1 and not node.is_end and path:
            only_char = next(iter(node.children))
            only_child = node.children[only_char]
            node.fragment += only_child.fragment
            node.children = only_child.children
            node.is_end = only_child.is_end
            node.value = only_child.value
        return True

    def keys_with_prefix(self, prefix: str) -> Iterator[str]:
        """Yield all keys that begin with *prefix*, lazily."""
        node = self._find_node(prefix)
        if node is None:
            return
        # DFS with explicit stack: (node, accumulated_prefix)
        stack: list[tuple[_TrieNode, str]] = [(node, prefix)]
        while stack:
            current, acc = stack.pop()
            if current.is_end:
                yield acc
            for ch in sorted(current.children, reverse=True):
                child = current.children[ch]
                stack.append((child, acc + child.fragment))

    def __len__(self) -> int:
        return self._size

    def __contains__(self, key: str) -> bool:
        return self.search(key) is not None

    def __iter__(self) -> Iterator[str]:
        return self.keys_with_prefix("")

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _find_node(self, key: str) -> _TrieNode | None:
        """Walk the trie following *key*; return the landing node or None."""
        node = self._root
        i = 0
        while i < len(key):
            char = key[i]
            if char not in node.children:
                return None
            child = node.children[char]
            fragment = child.fragment
            j = 0
            while j < len(fragment) and i + j < len(key) and key[i + j] == fragment[j]:
                j += 1
            if j < len(fragment):
                # We're *inside* a compressed edge — valid for prefix queries
                # but not for exact-node queries.  For `starts_with` we still
                # want to return the child when the remaining key is fully
                # consumed, so check that.
                if i + j == len(key):
                    return child
                return None
            node = child
            i += j
        return node


# ------------------------------------------------------------------
# Quick demo
# ------------------------------------------------------------------

if __name__ == "__main__":
    trie = Trie()

    words = ["apple", "app", "application", "apply", "ape", "bat", "batch", "bath"]
    for w in words:
        trie.insert(w, w.upper())

    print(f"Trie size: {len(trie)}")
    print(f"search('apple')      → {trie.search('apple')}")
    print(f"search('app')        → {trie.search('app')}")
    print(f"search('apex')       → {trie.search('apex')}")
    print(f"starts_with('app')   → {trie.starts_with('app')}")
    print(f"starts_with('xyz')   → {trie.starts_with('xyz')}")
    print(f"keys_with_prefix('app') → {sorted(trie.keys_with_prefix('app'))}")
    print(f"keys_with_prefix('ba')  → {sorted(trie.keys_with_prefix('ba'))}")

    trie.delete("app")
    print(f"\nAfter deleting 'app':")
    print(f"search('app')        → {trie.search('app')}")
    print(f"search('apple')      → {trie.search('apple')}")
    print(f"keys_with_prefix('app') → {sorted(trie.keys_with_prefix('app'))}")
