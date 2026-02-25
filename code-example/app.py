"""
Trie Lookup Service — A REST API for prefix-based autocomplete.

Exposes the compressed Trie data structure as a JSON API with endpoints
for inserting words, searching, prefix-based autocompletion, and deletion.
Built with Flask. Designed for containerized deployment.
"""

from __future__ import annotations

import os
import time
import logging

from flask import Flask, jsonify, request

# ---------------------------------------------------------------------------
# Trie implementation (path-compressed, iterative)
# ---------------------------------------------------------------------------

from dataclasses import dataclass, field
from typing import Any, Iterator


@dataclass
class _TrieNode:
    children: dict[str, _TrieNode] = field(default_factory=dict)
    is_end: bool = False
    value: Any = None
    fragment: str = ""


class Trie:
    """Compressed prefix tree mapping string keys → values."""

    def __init__(self) -> None:
        self._root = _TrieNode()
        self._size = 0

    def insert(self, key: str, value: Any = True) -> None:
        node = self._root
        i = 0
        while i < len(key):
            char = key[i]
            if char not in node.children:
                leaf = _TrieNode(fragment=key[i:], is_end=True, value=value)
                node.children[char] = leaf
                self._size += 1
                return
            child = node.children[char]
            fragment = child.fragment
            j = 0
            while j < len(fragment) and i + j < len(key) and key[i + j] == fragment[j]:
                j += 1
            if j == len(fragment):
                node = child
                i += j
            else:
                split = _TrieNode(fragment=fragment[:j])
                split.children[fragment[j]] = child
                child.fragment = fragment[j:]
                node.children[char] = split
                if i + j == len(key):
                    split.is_end = True
                    split.value = value
                    self._size += 1
                    return
                remaining = key[i + j:]
                new_leaf = _TrieNode(fragment=remaining, is_end=True, value=value)
                split.children[remaining[0]] = new_leaf
                self._size += 1
                return
        if not node.is_end:
            self._size += 1
        node.is_end = True
        node.value = value

    def search(self, key: str) -> Any | None:
        node = self._find_node(key)
        if node is not None and node.is_end:
            return node.value
        return None

    def starts_with(self, prefix: str) -> bool:
        return self._find_node(prefix) is not None

    def delete(self, key: str) -> bool:
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
        while path and not node.children and not node.is_end:
            parent, edge_char = path.pop()
            del parent.children[edge_char]
            node = parent
        if len(node.children) == 1 and not node.is_end and path:
            only_char = next(iter(node.children))
            only_child = node.children[only_char]
            node.fragment += only_child.fragment
            node.children = only_child.children
            node.is_end = only_child.is_end
            node.value = only_child.value
        return True

    def keys_with_prefix(self, prefix: str) -> Iterator[str]:
        node = self._find_node(prefix)
        if node is None:
            return
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

    def _find_node(self, key: str) -> _TrieNode | None:
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
                if i + j == len(key):
                    return child
                return None
            node = child
            i += j
        return node


# ---------------------------------------------------------------------------
# Flask application
# ---------------------------------------------------------------------------

app = Flask(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("trie-service")

# Global trie instance — persists for the lifetime of the process
trie = Trie()
_start_time = time.time()

# Seed with sample data so the service is useful out-of-the-box
_SEED_WORDS = [
    "algorithm", "api", "application", "array", "authentication",
    "binary", "branch", "buffer", "build", "byte",
    "cache", "callback", "class", "client", "compiler",
    "container", "cpu", "database", "debug", "deploy",
    "docker", "endpoint", "exception", "flask", "function",
    "gateway", "git", "graph", "hash", "heap",
    "index", "interface", "json", "kernel", "lambda",
    "linked-list", "load-balancer", "memory", "microservice", "middleware",
    "node", "object", "parser", "pipeline", "pointer",
    "prefix-tree", "process", "queue", "recursion", "redis",
    "request", "response", "rest", "router", "runtime",
    "schema", "server", "socket", "stack", "stream",
    "thread", "token", "tree", "trie", "tuple",
    "upstream", "variable", "version", "webhook", "worker",
]

for word in _SEED_WORDS:
    trie.insert(word, word)
logger.info("Seeded trie with %d words", len(_SEED_WORDS))


# ── Health & Info ─────────────────────────────────────────────────────────

@app.route("/")
def index():
    """Landing page with API documentation."""
    return jsonify({
        "service": "Trie Lookup Service",
        "version": "1.0.0",
        "description": "REST API for prefix-based autocomplete powered by a compressed Trie",
        "endpoints": {
            "GET  /":                "This help page",
            "GET  /health":          "Health check",
            "GET  /stats":           "Trie statistics",
            "GET  /search?q=<key>":  "Exact match lookup",
            "GET  /prefix?q=<pfx>":  "Autocomplete — all keys starting with prefix",
            "POST /insert":          "Insert a key  {\"key\": \"...\", \"value\": \"...\"}",
            "DELETE /delete?q=<key>":"Delete a key",
        },
    })


@app.route("/health")
def health():
    """Liveness / readiness probe."""
    return jsonify({
        "status": "healthy",
        "uptime_seconds": round(time.time() - _start_time, 2),
        "trie_size": len(trie),
    })


@app.route("/stats")
def stats():
    """Trie statistics."""
    return jsonify({
        "total_keys": len(trie),
        "uptime_seconds": round(time.time() - _start_time, 2),
        "seed_words": len(_SEED_WORDS),
    })


# ── Core API ──────────────────────────────────────────────────────────────

@app.route("/search")
def search():
    """Exact key lookup."""
    q = request.args.get("q", "").strip().lower()
    if not q:
        return jsonify({"error": "Missing query parameter 'q'"}), 400
    result = trie.search(q)
    return jsonify({"key": q, "found": result is not None, "value": result})


@app.route("/prefix")
def prefix():
    """Return all keys sharing a given prefix (autocomplete)."""
    q = request.args.get("q", "").strip().lower()
    limit = request.args.get("limit", "25", type=str)
    try:
        limit = int(limit)
    except ValueError:
        limit = 25

    if not q:
        return jsonify({"error": "Missing query parameter 'q'"}), 400

    matches = []
    for key in trie.keys_with_prefix(q):
        matches.append(key)
        if len(matches) >= limit:
            break

    return jsonify({
        "prefix": q,
        "count": len(matches),
        "matches": matches,
    })


@app.route("/insert", methods=["POST"])
def insert():
    """Insert a key into the trie."""
    body = request.get_json(silent=True) or {}
    key = body.get("key", "").strip().lower()
    value = body.get("value", key)

    if not key:
        return jsonify({"error": "Missing 'key' in request body"}), 400
    if len(key) > 256:
        return jsonify({"error": "Key too long (max 256 chars)"}), 400

    trie.insert(key, value)
    logger.info("Inserted key=%s", key)
    return jsonify({"inserted": key, "value": value, "trie_size": len(trie)}), 201


@app.route("/delete", methods=["DELETE"])
def delete():
    """Delete a key from the trie."""
    q = request.args.get("q", "").strip().lower()
    if not q:
        return jsonify({"error": "Missing query parameter 'q'"}), 400

    deleted = trie.delete(q)
    status = 200 if deleted else 404
    return jsonify({"key": q, "deleted": deleted, "trie_size": len(trie)}), status


# ---------------------------------------------------------------------------
# Entrypoint
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    debug = os.environ.get("FLASK_DEBUG", "0") == "1"
    logger.info("Starting Trie Lookup Service on port %d", port)
    app.run(host="0.0.0.0", port=port, debug=debug)
