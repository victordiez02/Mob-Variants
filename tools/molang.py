"""Tiny Molang evaluator (subset used by render controllers) to simulate what each mob renders."""
import re, math

TOK = re.compile(r"\s*(?:(\d+\.\d*|\.\d+|\d+)|('[^']*')|([A-Za-z_][A-Za-z0-9_.]*)|(&&|\|\||==|!=|<=|>=|\?\?|[-+*/!<>?:()\[\],;]))")

class P:
    def __init__(self, s, env):
        self.t = []; pos = 0
        while pos < len(s):
            m = TOK.match(s, pos)
            if not m or m.end() == pos:
                if s[pos:].strip() == "": break
                raise SyntaxError(f"bad token at {s[pos:pos+20]!r}")
            pos = m.end()
            num, st, ident, op = m.groups()
            if num is not None: self.t.append(("n", float(num)))
            elif st is not None: self.t.append(("s", st[1:-1]))
            elif ident is not None: self.t.append(("i", ident))
            elif op is not None: self.t.append(("o", op))
        self.i = 0; self.env = env
    def peek(self): return self.t[self.i] if self.i < len(self.t) else (None, None)
    def eat(self, v=None):
        k, x = self.peek()
        if v is not None and x != v: raise SyntaxError(f"expected {v} got {x}")
        self.i += 1; return x
    def expr(self): return self.ternary()
    def ternary(self):
        c = self.null()
        if self.peek()[1] == "?":
            self.eat("?"); a = self.ternary()
            if self.peek()[1] == ":":
                self.eat(":"); b = self.ternary()
            else:
                b = 0.0
            return a if truthy(c) else b
        return c
    def null(self):
        a = self.orr()
        while self.peek()[1] == "??":
            self.eat(); b = self.orr(); a = b if a is None else a
        return a
    def orr(self):
        a = self.andd()
        while self.peek()[1] == "||":
            self.eat(); b = self.andd(); a = 1.0 if truthy(a) or truthy(b) else 0.0
        return a
    def andd(self):
        a = self.cmp()
        while self.peek()[1] == "&&":
            self.eat(); b = self.cmp(); a = 1.0 if truthy(a) and truthy(b) else 0.0
        return a
    def cmp(self):
        a = self.add()
        while self.peek()[1] in ("==", "!=", "<", ">", "<=", ">="):
            op = self.eat(); b = self.add()
            a = 1.0 if {"==": a == b, "!=": a != b, "<": num(a) < num(b), ">": num(a) > num(b), "<=": num(a) <= num(b), ">=": num(a) >= num(b)}[op] else 0.0
        return a
    def add(self):
        a = self.mul()
        while self.peek()[1] in ("+", "-"):
            op = self.eat(); b = self.mul(); a = num(a) + num(b) if op == "+" else num(a) - num(b)
        return a
    def mul(self):
        a = self.unary()
        while self.peek()[1] in ("*", "/"):
            op = self.eat(); b = self.unary(); a = num(a) * num(b) if op == "*" else (num(a) / num(b) if num(b) else 0.0)
        return a
    def unary(self):
        if self.peek()[1] == "!": self.eat(); return 0.0 if truthy(self.unary()) else 1.0
        if self.peek()[1] == "-": self.eat(); return -num(self.unary())
        return self.post()
    def post(self):
        k, x = self.peek()
        if x == "(":
            self.eat(); v = self.expr(); self.eat(")"); return v
        if k == "n": self.eat(); return x
        if k == "s": self.eat(); return x
        if k == "i":
            self.eat(); name = x.lower()
            args = None
            if self.peek()[1] == "(":
                self.eat(); args = []
                while self.peek()[1] != ")":
                    args.append(self.expr())
                    if self.peek()[1] == ",": self.eat()
                self.eat(")")
            if self.peek()[1] == "[":
                self.eat(); idx = self.expr(); self.eat("]")
                arr = self.env["arrays"].get(name)
                if arr is None: raise KeyError("array " + name)
                n = int(math.floor(num(idx)))
                n = max(n, 0) % len(arr)   # Bedrock: index = max(0, x) % size
                return self.env["resolve"](arr[n])
            return self.env["lookup"](name, args)
        raise SyntaxError(f"unexpected {x!r}")

def num(v):
    if isinstance(v, str): return 0.0
    return float(v or 0.0)
def truthy(v):
    if isinstance(v, str): return True
    return bool(v)

def evaluate(s, env):
    p = P(s, env); v = p.expr()
    return v
