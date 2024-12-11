class WatGenerator:
    def __init__(self):
        self.wat_content = []
        self.indent_level = 0

    def indent(self):
        return '  ' * self.indent_level

    def generate_wat(self, ast, filename):
        self.wat_content.append("(module")
        self.indent_level += 1
        self.wat_content.append(f"{self.indent()}(memory $mem 1)")
        self.wat_content.append(f"{self.indent()}(export \"memory\" (memory $mem))")
        
        for node in ast.parts:  
            self.visit(node)

        self.indent_level -= 1
        self.wat_content.append(")")

        with open(filename, 'w') as f:
            f.write("\n".join(self.wat_content))

    def visit(self, node):
        method_name = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method_name, self.generic_visit)
        visitor(node)

    def generic_visit(self, node):
        raise Exception(f'No visit_{node.__class__.__name__} method')

    def visit_Block(self, node):
        for stmt in node.stmts:
            self.visit(stmt)

    def visit_Func(self, func):
        params = " ".join(f"(param ${p.id} i32)" for p in func.params)
        results = "(result i32)"
        self.wat_content.append(f"{self.indent()}(func ${func.id.id} {params} {results}")
        self.indent_level += 1
        self.visit(func.body)
        self.indent_level -= 1
        self.wat_content.append(f"{self.indent()})")
        self.wat_content.append(f"{self.indent()}(export \"{func.id.id}\" (func ${func.id.id}))")

    def visit_Main(self, node):
        self.visit(node.body)

    def visit_BinExpr(self, bin_op):
        operation_map = {
            '+': 'i32.add',
            '-': 'i32.sub',
            '*': 'i32.mul',
            '/': 'i32.div_s',
            '%': 'i32.rem_s'
        }
        operation = operation_map.get(bin_op.op, 'i32.add')
        self.wat_content.append(f"{self.indent()}({operation}")
        self.indent_level += 1
        self.visit(bin_op.left)
        self.visit(bin_op.right)
        self.indent_level -= 1
        self.wat_content.append(f"{self.indent()})")

    def visit_IntNum(self, num):
        self.wat_content.append(f"{self.indent()}(i32.const {num.value})")

    def visit_FloatNum(self, num):
        self.wat_content.append(f"{self.indent()}(f32.const {num.value})")

    def visit_Id(self, identifier):
        self.wat_content.append(f"{self.indent()}(local.get ${identifier.id})")

    def visit_AssignExpr(self, assign):
        self.wat_content.append(f"{self.indent()}(local.get ${assign.id.id}")
        self.indent_level += 1
        self.visit(assign.value)
        self.indent_level -= 1
        self.wat_content.append(f"{self.indent()})")

    def visit_Return(self, ret):
        self.wat_content.append(f"{self.indent()}(return ")
        self.indent_level += 1
        self.visit(ret.expr)
        self.indent_level -= 1
        self.wat_content.append(f"{self.indent()})")
