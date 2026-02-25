# Code Examples Documentation

## `code-example/trie.py`

**Language:** Python 3.10+  
**Purpose:** A compressed prefix tree (Patricia/Radix Trie) that maps arbitrary string keys to arbitrary values.  
**Dependencies:** Standard library only (`dataclasses`, `typing`).

### Description

`trie.py` implements a **path-compressed Trie** (also known as a Radix Tree or Patricia Tree). Instead of storing one character per node, consecutive single-child nodes are collapsed into a single node holding a multi-character **fragment**. This reduces memory consumption and speeds up lookups on keys with long shared prefixes.

Key design choices:

| Technique | Details |
|---|---|
| **Path compression** | Chains of single-child nodes are merged into one node with a `fragment` label. |
| **Iterative traversal** | All public methods use `while` loops instead of recursion — O(1) stack space. |
| **Lazy generator enumeration** | `keys_with_prefix` and `__iter__` yield results via an explicit DFS stack, keeping memory low for large tries. |

**Complexity**

| Operation | Time |
|---|---|
| `insert(key)` | O(n) — n = key length |
| `search(key)` | O(n) |
| `delete(key)` | O(n) |
| `starts_with(prefix)` | O(n) |
| `keys_with_prefix(prefix)` | O(n + m) — m = number of matches |

### Public API

```python
trie = Trie()

trie.insert("apple", 1)      # map "apple" → 1
trie.search("apple")         # → 1   (None if absent)
trie.starts_with("app")      # → True
trie.delete("apple")         # → True (False if key not found)
list(trie.keys_with_prefix("app"))  # → ["app", "application", ...]
len(trie)                    # number of inserted keys
"apple" in trie              # membership test via __contains__
list(trie)                   # all keys via __iter__
```

### Key Classes

#### `_TrieNode` (internal dataclass)

```python
@dataclass
class _TrieNode:
    children: dict[str, _TrieNode]  # keyed by first char of child's fragment
    is_end: bool                    # True if this node terminates a key
    value: Any                      # stored value for terminal nodes
    fragment: str                   # compressed edge label from parent
```

#### `Trie`

The public class. Maintains a `_root` `_TrieNode` and a `_size` counter.  
Internal helper `_find_node(key)` walks the tree and returns the landing node (or `None`), shared by `search`, `starts_with`, `delete`, and `keys_with_prefix`.

---

### Diagrams

#### Data structure layout

The diagram below shows the compressed node structure after inserting `"app"`, `"apple"`, `"application"`, and `"apply"`.

```mermaid
classDiagram
    class _TrieNode {
        +dict children
        +bool is_end
        +Any value
        +str fragment
    }

    class Root {
        fragment: ""
        is_end: false
    }

    class NodeA {
        fragment: "a"
        is_end: false
    }

    class NodeApp {
        fragment: "pp"
        is_end: true
        value: 2
    }

    class NodeApple {
        fragment: "le"
        is_end: true
        value: 1
    }

    class NodeApplica {
        fragment: "lica"
        is_end: false
    }

    class NodeApplication {
        fragment: "tion"
        is_end: true
        value: 3
    }

    class NodeApply {
        fragment: "y"
        is_end: true
        value: 4
    }

    Root --> NodeA : "a"
    NodeA --> NodeApp : "p"
    NodeApp --> NodeApple : "l"
    NodeApple --> NodeApplica : "i"
    NodeApp --> NodeApply : "y"
    NodeApplica --> NodeApplication : "t"
```

---

#### `insert` flowchart

Step-by-step control flow when inserting a new key into the trie.

```mermaid
flowchart TD
    A([Start: insert key]) --> B[Set node = root, i = 0]
    B --> C{i < len key?}
    C -- No --> M[Mark node.is_end = True\nstore value\nincrement size if new]
    M --> Z([Done])
    C -- Yes --> D[char = key i]
    D --> E{char in node.children?}
    E -- No --> F[Create leaf node\nfragment = key i ..\nAppend as child]
    F --> Z
    E -- Yes --> G[child = node.children char\nfragment = child.fragment]
    G --> H[Walk shared prefix\ncount matching chars j]
    H --> I{j == len fragment?}
    I -- Yes --> J[Entire fragment matched\nDescend: node = child\ni += j]
    J --> C
    I -- No --> K{i+j == len key?}
    K -- Yes --> L[Split node, mark split.is_end = True\nAttach old child with remaining fragment]
    L --> Z
    K -- No --> N[Split node\nCreate new leaf for remaining key suffix\nAttach both children to split]
    N --> Z
```

---

#### `delete` flowchart

The delete operation walks down tracking the parent path, removes the terminal marker, then cleans up orphaned nodes and re-merges single-child internal nodes bottom-up.

```mermaid
flowchart TD
    A([Start: delete key]) --> B[Walk trie, recording path\nof parent-edge pairs]
    B --> C{Key exists\nand node.is_end?}
    C -- No --> X([Return False])
    C -- Yes --> D[Set node.is_end = False\nnode.value = None\ndecrement size]
    D --> E{node has no children\nand not is_end?}
    E -- Yes --> F[Pop parent from path\nDelete edge to node\nnode = parent]
    F --> E
    E -- No --> G{node has exactly\none child and\nnot is_end and\nhas parent?}
    G -- Yes --> H[Merge single child into node\nConcatenate fragments\nInherit child's children/is_end/value]
    H --> Z([Return True])
    G -- No --> Z
```

---

#### `keys_with_prefix` sequence diagram

Walkthrough of enumerating all keys with prefix `"app"` from a trie containing `"app"`, `"apple"`, and `"apply"`.

```mermaid
sequenceDiagram
    participant Caller
    participant Trie
    participant Stack

    Caller->>Trie: keys_with_prefix("app")
    Trie->>Trie: _find_node("app") → NodeApp
    Trie->>Stack: push (NodeApp, "app")
    loop DFS until stack empty
        Stack-->>Trie: pop (NodeApp, "app")
        Trie-->>Caller: yield "app"  [is_end=True]
        Trie->>Stack: push (NodeApply, "apply")
        Trie->>Stack: push (NodeApple, "apple")
        Stack-->>Trie: pop (NodeApple, "apple")
        Trie-->>Caller: yield "apple"  [is_end=True]
        Stack-->>Trie: pop (NodeApply, "apply")
        Trie-->>Caller: yield "apply"  [is_end=True]
    end
```

---

#### `_find_node` state diagram

Internal traversal states while walking a compressed edge.

```mermaid
stateDiagram-v2
    [*] --> AtNode : start at root
    AtNode --> CheckChar : read key[i]
    CheckChar --> NoMatch : char not in children
    NoMatch --> [*] : return None
    CheckChar --> WalkFragment : child found
    WalkFragment --> FullMatch : j == len(fragment)
    WalkFragment --> PartialInsideEdge : j < len(fragment)
    PartialInsideEdge --> KeyExhausted : i+j == len(key)
    KeyExhausted --> [*] : return child (valid for starts_with)
    PartialInsideEdge --> [*] : return None (key diverges)
    FullMatch --> AtNode : descend — node = child, i += j
    AtNode --> [*] : i == len(key) → return node
```
