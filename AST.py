from dataclasses import dataclass

@dataclass
class Node:
    lineno: int

@dataclass
class Start(Node):
    parts: list

@dataclass
class Main(Node):
    body: Node

@dataclass
class IntNum(Node):
    value: int

@dataclass
class FloatNum(Node):
    value: float

@dataclass
class String(Node):
    value: str

@dataclass
class Block(Node):
    stmts: list

@dataclass
class Transposition(Node):
    target: Node

@dataclass
class UnaryMinus(Node):
    expr: Node

@dataclass
class BinExpr(Node):
    op: str
    left: Node
    right: Node

@dataclass
class Id(Node):
    id: str

    def __hash__(self):
        return hash(self.id)
    
    def __eq__(self, other):
        if isinstance(other, str):
            return self.id == other
        elif isinstance(other, Id):
            return self.id == other.id 
        return False

@dataclass
class Func(Node):
    id: Id
    params: list
    body: Node

@dataclass
class FnCall(Node):
    fn: Id
    args: list

@dataclass
class AssignExpr(Node):
    type: str
    id: Id
    value: Node

@dataclass
class ForLoop(Node):
    id: Id
    range: Node
    stmt: Node

@dataclass
class UntilLoop(Node):
    cond: Node
    stmt: Node

@dataclass
class Range(Node):
    min: Node
    max: Node

@dataclass
class IfStmt(Node):
    cond: Node
    positive: Node
    negative: Node = Block('0', [])

@dataclass
class Vector(Node):
    values: list

@dataclass
class Ref(Node):
    target: Node
    indices: list

@dataclass
class Return(Node):
    expr: Node

@dataclass
class Stop(Node):
    pass

@dataclass
class Skip(Node):
    pass

@dataclass
class Out(Node):
    args: list

@dataclass
class Error(Node):
    msg: str
      