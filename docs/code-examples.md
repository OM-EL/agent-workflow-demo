# Code Examples Documentation

This document describes every file inside the `code-example/` folder of this repository.

---

## `code-example/trie.py`

**Language:** Python 3.10+  
**Purpose:** Stand-alone implementation of a compressed Prefix Tree (Trie) with path compression, iterative traversal, and lazy generator-based enumeration.  
**Dependencies:** Standard library only (`dataclasses`, `typing`)

### Description

`trie.py` defines two classes:

| Class | Role |
|---|---|
| `_TrieNode` | Internal dataclass representing a single node. Stores child pointers, an end-of-word flag, the associated value, and a **fragment** string (the edge label used for path compression). |
| `Trie` | Public API. A compressed prefix tree that maps arbitrary string keys to arbitrary values. |

**Key techniques:**

- **Path compression** — consecutive single-child chains are collapsed into one node whose `fragment` holds the full shared substring. This reduces memory and speeds up traversal on long keys with common prefixes.
- **Iterative traversal** — `insert`, `search`, `delete`, and `_find_node` use `while` loops instead of recursion, keeping the call stack O(1) regardless of key length.
- **Generator-based enumeration** — `keys_with_prefix` and `__iter__` use an explicit DFS stack and `yield`, so even a trie holding millions of entries is enumerated lazily.

### Public API

```python
t = Trie()
t.insert("apple", 1)          # Insert key → value
t.search("apple")             # → 1  (None if absent)
t.starts_with("app")          # → True
t.delete("apple")             # → True if deleted
list(t.keys_with_prefix("ap"))# → ['app', 'apple', ...]
len(t)                        # → number of stored keys
"apple" in t                  # → bool (uses search)
```

### Complexity

| Operation | Time |
|---|---|
| `insert` / `search` / `delete` | O(n) — n = key length |
| `starts_with` | O(n) |
| `keys_with_prefix` | O(n + m) — m = number of matches |

### Diagrams

#### Data Structure Layout

The class diagram below shows the relationship between `Trie` and `_TrieNode`.

```mermaid
classDiagram
    class Trie {
        -_TrieNode _root
        -int _size
        +insert(key, value) None
        +search(key) Any
        +starts_with(prefix) bool
        +delete(key) bool
        +keys_with_prefix(prefix) Iterator
        +__len__() int
        +__contains__(key) bool
        +__iter__() Iterator
        -_find_node(key) _TrieNode
    }

    class _TrieNode {
        +dict children
        +bool is_end
        +Any value
        +str fragment
    }

    Trie "1" --> "1" _TrieNode : _root
    _TrieNode "1" --> "0..*" _TrieNode : children
```

#### Path-Compressed Tree Example

After inserting `"app"`, `"apple"`, and `"application"`, the internal tree looks like this (each box is a `_TrieNode`, edge labels are `fragment` values):

```mermaid
flowchart TD
    ROOT["ROOT\nfragment=''"]
    N1["node\nfragment='app'\nis_end=True (app)"]
    N2["node\nfragment='le'\nis_end=True (apple)"]
    N3["node\nfragment='lication'\nis_end=True (application)"]

    ROOT -->|"a"| N1
    N1 -->|"l"| N2
    N1 -->|"l"| N3
```

> Note: In practice `apple` and `application` share a further split on `"li"` vs `"le"`, but the diagram above illustrates the concept of fragment-labelled edges.

#### Insert Operation Flowchart

```mermaid
flowchart TD
    A([Start insert key]) --> B{Characters remaining\nin key?}
    B -- No --> C{node.is_end?}
    C -- No --> D[Set is_end=True\nincrement size]
    C -- Yes --> E[Update value only]
    D --> Z([Done])
    E --> Z

    B -- Yes --> F{First char\nin node.children?}
    F -- No --> G[Create leaf node\nwith remaining suffix\nincrement size]
    G --> Z

    F -- Yes --> H[Compare key suffix\nagainst child.fragment]
    H --> I{Full fragment\nmatched?}
    I -- Yes --> J[Descend into child\nadvance i by fragment length]
    J --> B

    I -- No --> K[Split node at\nmatch boundary]
    K --> L{Key exhausted\nat split point?}
    L -- Yes --> M[Mark split node\nas end, increment size]
    M --> Z
    L -- No --> N[Create new leaf\nfor remaining key suffix\nincrement size]
    N --> Z
```

#### Delete Operation Flowchart

```mermaid
flowchart TD
    A([Start delete key]) --> B[Walk trie, recording path]
    B --> C{Key fully\nmatched?}
    C -- No --> D([Return False])
    C -- Yes --> E{node.is_end?}
    E -- No --> D
    E -- Yes --> F[Unmark is_end\ndecrement size]
    F --> G{Node has\nno children?}
    G -- Yes --> H[Remove node\nfrom parent\nwalk up path]
    H --> G
    G -- No --> I{Node has exactly\none child & not end?}
    I -- Yes --> J[Merge node with\nits only child\npath compression]
    J --> K([Return True])
    I -- No --> K
```

#### Prefix Search (`keys_with_prefix`) — Sequence Walkthrough

The following sequence diagram shows how `keys_with_prefix("app")` yields results using an explicit DFS stack.

```mermaid
sequenceDiagram
    participant Caller
    participant Trie
    participant Stack

    Caller->>Trie: keys_with_prefix("app")
    Trie->>Trie: _find_node("app") → landing node N
    Trie->>Stack: push (N, "app")
    loop While stack not empty
        Stack-->>Trie: pop (current, acc)
        alt current.is_end
            Trie-->>Caller: yield acc
        end
        Trie->>Stack: push children (sorted desc) with acc+fragment
    end
```

---

## `code-example/app.py`

**Language:** Python 3.10+  
**Purpose:** Flask REST API that exposes the compressed Trie as a JSON autocomplete / lookup service. Designed for containerised deployment (reads `PORT` from environment, ships a pre-seeded word list).  
**Dependencies:** `flask` (third-party); `dataclasses`, `typing`, `os`, `time`, `logging` (standard library)

### Description

`app.py` embeds the same path-compressed `Trie` / `_TrieNode` implementation from `trie.py` directly in the file and wraps it with a Flask application. On startup it seeds the trie with ~70 common computing terms so the API is useful immediately.

**Global state:**

| Variable | Purpose |
|---|---|
| `trie` | Singleton `Trie` instance shared across all requests |
| `_start_time` | `time.time()` at process start, used by `/health` and `/stats` |
| `_SEED_WORDS` | List of ~70 seed terms inserted at import time |

### Endpoints

| Method | Path | Query / Body | Description |
|---|---|---|---|
| `GET` | `/` | — | JSON help page listing all endpoints |
| `GET` | `/health` | — | Liveness probe: `status`, `uptime_seconds`, `trie_size` |
| `GET` | `/stats` | — | Trie statistics: `total_keys`, `uptime_seconds`, `seed_words` |
| `GET` | `/search` | `?q=<key>` | Exact-match lookup; returns `found` bool and `value` |
| `GET` | `/prefix` | `?q=<pfx>&limit=<n>` | Autocomplete; returns up to `limit` (default 25) matching keys |
| `POST` | `/insert` | `{"key": "...", "value": "..."}` | Insert a key (max 256 chars); returns `trie_size` |
| `DELETE` | `/delete` | `?q=<key>` | Delete a key; 404 if not found |

### Example Usage

```bash
# Autocomplete
curl "http://localhost:8080/prefix?q=th"
# → {"prefix":"th","count":3,"matches":["thread","token","tree"]}

# Insert a custom word
curl -X POST http://localhost:8080/insert \
     -H "Content-Type: application/json" \
     -d '{"key": "terraform", "value": "infrastructure as code"}'

# Exact search
curl "http://localhost:8080/search?q=flask"
# → {"key":"flask","found":true,"value":"flask"}
```

### Diagrams

#### Service Architecture

```mermaid
flowchart TD
    Client([HTTP Client])
    Flask[Flask App\napp.py]
    TrieDS[(In-Memory Trie\nsingleton)]
    Seed[Seed Words\n~70 terms]

    Client -- "GET /search?q=..." --> Flask
    Client -- "GET /prefix?q=..." --> Flask
    Client -- "POST /insert" --> Flask
    Client -- "DELETE /delete?q=..." --> Flask
    Flask -- "search / starts_with\nkeys_with_prefix\ninsert / delete" --> TrieDS
    Seed -- "inserted at startup" --> TrieDS
```

#### Request Lifecycle — Autocomplete (`GET /prefix`)

```mermaid
sequenceDiagram
    participant Client
    participant Flask
    participant Trie

    Client->>Flask: GET /prefix?q=th&limit=10
    Flask->>Flask: validate q (not empty)
    Flask->>Trie: keys_with_prefix("th")
    loop Consume generator up to limit
        Trie-->>Flask: yield next matching key
    end
    Flask-->>Client: 200 JSON {prefix, count, matches}
```

#### Request Lifecycle — Insert (`POST /insert`)

```mermaid
sequenceDiagram
    participant Client
    participant Flask
    participant Trie

    Client->>Flask: POST /insert {key, value}
    Flask->>Flask: parse JSON body
    alt key missing or empty
        Flask-->>Client: 400 {error}
    else key > 256 chars
        Flask-->>Client: 400 {error: "Key too long"}
    else valid
        Flask->>Trie: insert(key, value)
        Flask-->>Client: 201 {inserted, value, trie_size}
    end
```

#### Endpoint Routing Overview

```mermaid
flowchart LR
    R{Route}
    R -->|GET /| H0[index\nAPI help JSON]
    R -->|GET /health| H1[health\nuptime + size]
    R -->|GET /stats| H2[stats\ntotal_keys]
    R -->|GET /search| H3[search\nexact lookup]
    R -->|GET /prefix| H4[prefix\nautocomplete]
    R -->|POST /insert| H5[insert\nadd key]
    R -->|DELETE /delete| H6[delete\nremove key]
```

#### Application Startup Sequence

```mermaid
sequenceDiagram
    participant OS
    participant Python
    participant Flask
    participant Trie

    OS->>Python: python app.py
    Python->>Trie: Trie() — create empty trie
    loop For each word in _SEED_WORDS (~70 words)
        Python->>Trie: insert(word, word)
    end
    Python->>Flask: app.run(host=0.0.0.0, port=$PORT)
    Flask-->>OS: Listening on port (default 8080)
```
