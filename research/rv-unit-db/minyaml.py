"""Minimal OpenRA MiniYaml loader with inheritance resolution.

Node = [key, value, children]. Supports Inherits / Inherits@X, `-Key` removal,
and merging of top-level definitions spread across several files.
"""
import glob


def parse(path):
    root = []
    stack = [(-1, root)]
    with open(path, encoding='utf-8', errors='ignore') as f:
        for raw in f:
            raw = raw.rstrip('\r\n')
            if raw.lstrip().startswith('#'):
                continue
            s = raw.split('#', 1)[0]
            if not s.strip():
                continue
            ind = len(s) - len(s.lstrip('\t'))
            st = s.strip()
            k, _, v = st.partition(':')
            node = [k.strip(), v.strip(), []]
            while stack[-1][0] >= ind:
                stack.pop()
            stack[-1][1].append(node)
            stack.append((ind, node[2]))
    return root


def copy(n):
    return [n[0], n[1], [copy(c) for c in n[2]]]


def merge(a, b):
    if b[1]:
        a[1] = b[1]
    for c in b[2]:
        if c[0].startswith('-'):
            a[2] = [x for x in a[2] if x[0] != c[0][1:]]
            continue
        m = [x for x in a[2] if x[0] == c[0]]
        if m:
            merge(m[0], c)
        else:
            a[2].append(copy(c))


def load(patterns):
    d = {}
    for g in patterns:
        for f in sorted(glob.glob(g)):
            for n in parse(f):
                if n[0] in d:
                    merge(d[n[0]], n)
                else:
                    d[n[0]] = copy(n)
    return d


def is_inherit(k):
    return k == 'Inherits' or k.startswith('Inherits@')


class Resolver:
    def __init__(self, defs):
        self.defs = defs
        self.cache = {}

    def __call__(self, name, _stack=()):
        if name in self.cache:
            return self.cache[name]
        if name in _stack:
            raise ValueError('inheritance loop: ' + ' > '.join(_stack + (name,)))
        n = self.defs[name]
        out = [name, '', []]
        for c in n[2]:
            if is_inherit(c[0]) and c[1] in self.defs:
                merge(out, self(c[1], _stack + (name,)))
        merge(out, [name, n[1], [c for c in n[2] if not is_inherit(c[0])]])
        self.cache[name] = out
        return out


def get(node, key, default=None):
    for c in node[2]:
        if c[0] == key:
            return c[1]
    return default


def child(node, key):
    for c in node[2]:
        if c[0] == key:
            return c
    return None


def traits(node, prefix):
    """Children whose key is `prefix` or `prefix@X`."""
    return [c for c in node[2] if c[0] == prefix or c[0].startswith(prefix + '@')]


def wdist(v):
    """'6c512' -> 6.5 cells; '1024' -> 1.0 cells."""
    if v is None or v == '':
        return None
    v = v.strip()
    if 'c' in v:
        a, b = v.split('c', 1)
        return int(a or 0) + int(b or 0) / 1024
    try:
        return int(v) / 1024
    except ValueError:
        return None


def split_list(v):
    return [x.strip() for x in (v or '').split(',') if x.strip()]
