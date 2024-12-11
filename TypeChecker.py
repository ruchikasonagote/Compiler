import AST
from SymbolTable import Scope
from collections import defaultdict
from dataclasses import dataclass

@dataclass
class ArrayT:
    dims: int
    eltype: any
    size: any

    def __hash__(self):
        return hash((self.dims, self.eltype, self.size))

AnyT = 'any'
IntT = 'int'
FloatT = 'float'
StringT = 'string'
RangeT = 'range'
BoolT = 'bool'

aaa = defaultdict(
    lambda: defaultdict(
        lambda: defaultdict(
            lambda: AnyT
        ))
)



for op in '+-*/%':
    aaa[op][IntT][IntT] = IntT
    aaa[op][IntT][FloatT] = FloatT
    aaa[op][FloatT][IntT] = FloatT
    aaa[op][FloatT][FloatT] = FloatT
aaa['*'][StringT][IntT] = StringT

for op in ['<', '<=', '>', '>=', '!=', '==']:
    aaa[op][IntT][IntT] = BoolT
    aaa[op][IntT][FloatT] = BoolT
    aaa[op][FloatT][FloatT] = BoolT
    aaa[op][FloatT][FloatT] = BoolT

for op in ['==', '!=']:
    aaa[op][StringT][StringT] = BoolT


class NodeVisitor(object):

    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):        
        if isinstance(node, list):
            for elem in node:
                self.visit(elem)
        else:
            for child in node.children:
                if isinstance(child, list):
                    for item in child:
                        if isinstance(item, AST.Node):
                            self.visit(item)
                elif isinstance(child, AST.Node):
                    self.visit(child)

class TypeChecker(NodeVisitor):
    def __init__(self):
        self.current_scope = Scope()
        self.loop_count = 0
        self.valid = True

    def show_error(self, msg):
        self.valid = False
        print(msg)

    def visit_IntNum(self, node):
        return IntT

    def visit_FloatNum(self, node):
        return FloatT

    def visit_String(self, node):
        return StringT

    def visit_Block(self, node):
        self.current_scope = Scope(self.current_scope)
        self.visit(node.stmts)
        return None

    def visit_Start(self, node):
        self.visit(node.parts)
        return None
    
    def visit_Func(self, node):
        self.push_scope()
        ret_types = set()
        for param in node.params:
            self.current_scope.put(param.id, AnyT)

        if isinstance(node.body, AST.Block):
            statements = node.body.stmts
        else:
            statements = [node.body]  

        for stmt in statements:
            ret_type = self.visit(stmt)
            if isinstance(stmt, AST.Return):
                ret_types.add(ret_type)

        self.pop_scope()
        node.ret_type = ret_types.pop() if len(ret_types) == 1 else AnyT

    def visit_FnCall(self, node):
        func_def = self.current_scope.get(node.fn.id)
        if not isinstance(func_def, AST.Func):
            self.show_error(f"Line {node.lineno}: Function '{node.fn.id}' is not defined")
            return AnyT

        if len(node.args) != len(func_def.params):
            self.show_error(f"Line {node.lineno}: Incorrect number of arguments for function '{node.fn.id}'")
        else:
            for arg, param in zip(node.args, func_def.params):
                arg_type = self.visit(arg)
                if arg_type != param.type:
                    self.show_error(f"Line {node.lineno}: Type mismatch for argument {param.id}, expected {param.type}, found {arg_type}")

        return func_def.ret_type
    
    def visit_Out(self, node):
        self.visit(node.args)
        return None

    def visit_Main(self, node):
        self.visit(node.body)
        # return None
   
    def visit_UnaryMinus(self, node):
        type1 = self.visit(node.expr)
        if type1 not in [FloatT, IntT]: #  or not isinstance(type1, ArrayT)
            self.show_error(f'Line {node.line}: Can not apply unary minus to {type1}')
        return type1

    def visit_BinExpr(self, node):
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)
        result_type = aaa[node.op][left_type][right_type]
        return result_type

    def visit_Id(self, node):
        type1 = self.current_scope.get(node.id)
        if type1 == None:
            self.show_error(f'Line {node.line}: Variable can not be found in current scope')
            return AnyT
        return type1
    
    def visit_AssignExpr(self, node):
        value_type = self.visit(node.value)
        self.current_scope.put(node.id.id, value_type)
        return value_type
    
    def visit_IfStmt(self, node):
        condt = self.visit(node.cond)
        if condt != BoolT:
            self.show_error(f'Line {node.line}: If must have condition resolving to boolean value, but got {condt}')

        self.push_scope()
        self.visit(node.positive)
        self.pop_scope()

        self.push_scope()
        self.visit(node.negative) 
        self.pop_scope()

        return None

    def visit_ForLoop(self, node):
        self.loop_count += 1
        type1 = self.visit(node.range)
        if type1 != 'range':
            self.show_error(f'Line {node.line}: For loop must be iterating over range, but got {type1}')

        self.push_scope()
        self.current_scope.put(node.id.id, IntT)

        self.visit(node.stmt)

        self.pop_scope()
        self.loop_count -= 1
        return None

    def visit_UntilLoop(self, node):
        self.loop_count += 1

        condt = self.visit(node.cond)
        if condt != BoolT:
            self.show_error(f'Line {node.line}: While loop must have condition resolving to boolean value, but got {condt}')

        self.push_scope()
        self.visit(node.stmt)
        self.pop_scope()

        self.loop_count -= 1
        return None

    def visit_Range(self, node):
        if not self.visit(node.min) == self.visit(node.max) == IntT:
            self.show_error(f"Line {node.line}: Range extremas must be integers")
        return RangeT
    
    def visit_Vector(self, node):
        types = list(map(self.visit, node.values))
        eltype = types[0]
        if any(eltype != t for t in types):
            if isinstance(eltype, ArrayT):
                self.show_error(f"Line {node.line}: Inconsistant vector lengths, choosing first length to fit dimension")
                return ArrayT(eltype.dims + 1, eltype.eltype, (len(types),) + eltype.size)
            self.show_error(f'Line {node.line}: Inconsistant vector value types, choosing any as vector base type')
            return ArrayT(1, AnyT, (len(types),))
        if isinstance(eltype, ArrayT):
            return ArrayT(eltype.dims + 1, eltype.eltype, (len(types),) + eltype.size)
        return ArrayT(1, eltype, (len(types),))

    def visit_Stop(self, node):
        if self.loop_count == 0:
            self.show_error(f"Line {node.line}: Line {node.line}: Using break outside of loop")
        return None

    def visit_Skip(self, node):
        if self.loop_count == 0:
            self.show_error(f"Line {node.line}: Using continue outside of loop")
        return None
    
    def visit_Ref(self, node):
        targett = self.current_scope.get(node.target.id) if isinstance(node.target, AST.Id) else self.visit(node.target)

        if targett == StringT and len(node.indices) != 1:
            self.show_error(f"Line {node.line}: Indexing string with {len(node.indices)} dimensions")
            return IntT
        if isinstance(targett, ArrayT): 
            if len(node.indices) != targett.dims:
                self.show_error(f"Line {node.line}: Indexing {targett.dims}d array with {len(node.indices)} dimensions")
            
            for idx, m in zip(node.indices, targett.size):
                if isinstance(idx, AST.Range):
                    if not 0 <= idx.min.value <= idx.max.value < m:
                        self.show_error(f"Line {node.line}: Index out of range")
                        return targett.eltype
                else:
                    if not 0 <= idx.value < m:
                        self.show_error(f"Line {node.line}: Index out of range")
                        return targett.eltype

            return targett.eltype
        self.show_error(f"Line {node.line}: {targett} is not indexable")
        return AnyT
    
    def visit_Return(self, node):
        return self.visit(node.expr)

    def push_scope(self):
        self.current_scope = Scope(self.current_scope)
    
    def pop_scope(self):
        self.current_scope = self.current_scope.parent
