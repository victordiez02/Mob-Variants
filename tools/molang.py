"""Small Molang evaluator: the subset used by render controllers, entity scripts and pose animations.

Values are float or str ('temperate', Texture.x references…). Unknown names resolve through the
`Env.lookup` callback, so the caller decides what each query/variable returns.
"""
from __future__ import annotations

import math
import re
from functools import lru_cache
from collections.abc import Callable

Value = float | str
Lookup = Callable[[str, "list[Value] | None"], Value]

_TOK = re.compile(r"\s*(?:(\d+\.\d*f?|\.\d+f?|\d+f?)|('[^']*')|([A-Za-z_][A-Za-z0-9_.]*)"
                  r"|(&&|\|\||==|!=|<=|>=|\?\?|->|[-+*/!<>?:()\[\],;={}]))")


class Env:
    """Evaluation context.

    lookup(name, args): value of a query/variable/function (name lower-cased, args None if no call).
    arrays: render-controller arrays ({"array.skins": ["Texture.a", …]}).
    resolve(item): value of an array element (default: look it up as a name).
    """

    def __init__(self, lookup: Lookup, arrays: dict[str, list[str]] | None = None,
                 resolve: Callable[[str], Value] | None = None):
        self.lookup = lookup
        self.arrays = {k.lower(): v for k, v in (arrays or {}).items()}
        self.resolve: Callable[[str], Value] = resolve or (lambda x: lookup(x.lower(), None))


def num(v: Value | None) -> float:
    return 0.0 if v is None or isinstance(v, str) else float(v)


def truthy(v: Value | None) -> bool:
    return True if isinstance(v, str) else bool(v)


@lru_cache(maxsize=4096)
def _tokens(s: str) -> tuple[tuple[str, Value], ...]:
    out: list[tuple[str, Value]] = []
    pos = 0
    while pos < len(s):
        m = _TOK.match(s, pos)
        if not m or m.end() == pos:
            if s[pos:].strip() == "":
                break
            raise SyntaxError(f"bad token at {s[pos:pos + 20]!r}")
        pos = m.end()
        n, st, ident, op = m.groups()
        if n is not None:
            out.append(("n", float(n.rstrip("f"))))
        elif st is not None:
            out.append(("s", st[1:-1]))
        elif ident is not None:
            out.append(("i", ident))
        elif op is not None:
            out.append(("o", op))
    return tuple(out)


_MATH: dict[str, Callable[[list[float]], float]] = {
    "abs": lambda a: abs(a[0]), "floor": lambda a: float(math.floor(a[0])), "ceil": lambda a: float(math.ceil(a[0])),
    "round": lambda a: float(round(a[0])), "trunc": lambda a: float(math.trunc(a[0])),
    "mod": lambda a: math.fmod(a[0], a[1]) if a[1] else 0.0, "clamp": lambda a: min(max(a[0], a[1]), a[2]),
    "min": lambda a: min(a[0], a[1]), "max": lambda a: max(a[0], a[1]), "sqrt": lambda a: math.sqrt(max(a[0], 0)),
    "sin": lambda a: math.sin(math.radians(a[0])), "cos": lambda a: math.cos(math.radians(a[0])),
    "lerp": lambda a: a[0] + (a[1] - a[0]) * a[2], "pow": lambda a: a[0] ** a[1], "exp": lambda a: math.exp(a[0]),
    "pi": lambda a: math.pi, "sign": lambda a: math.copysign(1.0, a[0]),
}


class _Parser:
    def __init__(self, s: str, env: Env):
        self.t = _tokens(s)
        self.i = 0
        self.env = env
        self.skip = 0  # > 0 while parsing a branch that is not evaluated (Molang is lazy)

    def peek(self) -> Value | None:
        return self.t[self.i][1] if self.i < len(self.t) else None

    def kind(self) -> str | None:
        return self.t[self.i][0] if self.i < len(self.t) else None

    def eat(self, v: str | None = None) -> Value:
        x = self.peek()
        if self.i >= len(self.t) or (v is not None and x != v):
            raise SyntaxError(f"expected {v} got {x}")
        self.i += 1
        return x  # type: ignore[return-value]

    def done(self) -> bool:
        return self.i >= len(self.t)

    # statements: `a = expr; b = expr; expr`; `return expr`
    def statements(self) -> Value:
        last: Value = 0.0
        while not self.done():
            if self.peek() == ";":
                self.eat()
                continue
            if self.peek() == "return":
                self.eat()
                return self.expr()
            if self.kind() == "i" and self.i + 1 < len(self.t) and self.t[self.i + 1][1] == "=":
                name = str(self.eat()).lower()
                self.eat("=")
                val = self.expr()
                if not self.skip:
                    self.env.lookup("=" + name, [val])  # assignment hook
                last = val
            else:
                last = self.expr()
        return last

    def expr(self) -> Value:
        c = self.null()
        if self.peek() == "?":
            self.eat("?")
            take = truthy(c)
            a = self.lazy(not take, self.expr)
            b: Value = 0.0
            if self.peek() == ":":
                self.eat(":")
                b = self.lazy(take, self.expr)
            return a if take else b
        return c

    def lazy(self, skip: bool, fn: Callable[[], Value]) -> Value:
        self.skip += skip
        try:
            return fn()
        finally:
            self.skip -= skip

    def null(self) -> Value:
        a = self.orr()
        while self.peek() == "??":
            self.eat()
            b = self.orr()
            a = b if a is None else a
        return a

    def orr(self) -> Value:
        a = self.andd()
        while self.peek() == "||":
            self.eat()
            first = truthy(a)
            b = self.lazy(first, self.andd)
            a = 1.0 if first or truthy(b) else 0.0
        return a

    def andd(self) -> Value:
        a = self.cmp()
        while self.peek() == "&&":
            self.eat()
            first = truthy(a)
            b = self.lazy(not first, self.cmp)
            a = 1.0 if first and truthy(b) else 0.0
        return a

    def cmp(self) -> Value:
        a = self.add()
        while self.peek() in ("==", "!=", "<", ">", "<=", ">="):
            op = self.eat()
            b = self.add()
            r = {"==": a == b, "!=": a != b, "<": num(a) < num(b), ">": num(a) > num(b),
                 "<=": num(a) <= num(b), ">=": num(a) >= num(b)}[str(op)]
            a = 1.0 if r else 0.0
        return a

    def add(self) -> Value:
        a = self.mul()
        while self.peek() in ("+", "-"):
            op = self.eat()
            b = self.mul()
            a = num(a) + num(b) if op == "+" else num(a) - num(b)
        return a

    def mul(self) -> Value:
        a = self.unary()
        while self.peek() in ("*", "/"):
            op = self.eat()
            b = self.unary()
            a = num(a) * num(b) if op == "*" else (num(a) / num(b) if num(b) else 0.0)
        return a

    def unary(self) -> Value:
        if self.peek() == "!":
            self.eat()
            return 0.0 if truthy(self.unary()) else 1.0
        if self.peek() == "-":
            self.eat()
            return -num(self.unary())
        return self.post()

    def post(self) -> Value:
        k, x = self.kind(), self.peek()
        if x == "(":
            self.eat()
            v = self.expr()
            self.eat(")")
            return v
        if k in ("n", "s") and x is not None:
            self.eat()
            return x
        if k == "i":
            name = str(self.eat()).lower()
            args: list[Value] | None = None
            if self.peek() == "(":
                self.eat()
                args = []
                while self.peek() != ")":
                    args.append(self.expr())
                    if self.peek() == ",":
                        self.eat()
                self.eat(")")
            if self.peek() == "[":
                self.eat()
                idx = self.expr()
                self.eat("]")
                if self.skip:
                    return 0.0
                arr = self.env.arrays.get(name)
                if not arr:
                    raise KeyError("array " + name)
                n = max(int(math.floor(num(idx))), 0) % len(arr)  # Bedrock: max(0, x) % size
                return self.env.resolve(arr[n])
            if self.skip:
                return 0.0
            head, _, fn = name.partition(".")
            if head == "math" and fn in _MATH:
                return _MATH[fn]([num(a) for a in (args or [])] + [0.0, 0.0, 0.0])
            return self.env.lookup(name, args)
        raise SyntaxError(f"unexpected {x!r}")


def evaluate(s: str | float | int | bool, env: Env) -> Value:
    """Evaluate an expression or a list of `;`-separated statements."""
    if isinstance(s, bool):
        return 1.0 if s else 0.0
    if isinstance(s, (int, float)):
        return float(s)
    return _Parser(s, env).statements()
