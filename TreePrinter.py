import AST

def addToClass(cls):
    def decorator(func):
        setattr(cls,func.__name__,func)
        return func
    return decorator

class TreePrinter:

    @addToClass(AST.Node)
    def printTree(self, indent=0):
        raise Exception("printTree not defined in class " + self.__class__.__name__)


    @addToClass(AST.IntNum)
    def printTree(self, indent=0):
        print("|  " * indent + str(self.value))

    @addToClass(AST.FloatNum)
    def printTree(self, indent=0):
        print("|  " * indent + str(self.value))

    @addToClass(AST.String)
    def printTree(self, indent=0):
        print("|  " * indent + self.value)

    @addToClass(AST.Block)
    def printTree(self, indent=0):
        # print("|  " * indent + "BLOCK")
        # for i in self.stmts:
        #     i.printTree(indent + 1)
        for i in self.stmts:
            i.printTree(indent)

    @addToClass(AST.Main)
    def printTree(self, indent=0):
        print("|  " * indent + "MAIN")
        self.body.printTree(indent+1)

    @addToClass(AST.Start)
    def printTree(self, indent=0):
        # print("|  " * indent + "START")
        # self.parts.printTree()
        # print("|  " * indent + 'OUT')
        for i in self.parts:
            i.printTree()


    @addToClass(AST.FnCall)
    def printTree(self, indent=0):
        print("|  " * indent + "FNCALL")
        self.fn.printTree(indent + 1)
        for i in self.args:
            i.printTree(indent + 1)

    @addToClass(AST.Out)
    def printTree(self, indent=0):
        print("|  " * indent + 'OUT')
        for i in self.args:
            i.printTree(indent + 1)

    @addToClass(AST.UnaryMinus)
    def printTree(self, indent=0):
        print("|  " * indent + "UNARYMINUS")
        self.expr.printTree(indent + 1)
        
    @addToClass(AST.BinExpr)
    def printTree(self, indent=0):
        print("|  " * indent + self.op)
        self.left.printTree(indent + 1)
        self.right.printTree(indent + 1)

    @addToClass(AST.Id)
    def printTree(self, indent=0):
        print("|  " * indent + str(self.id))

    @addToClass(AST.AssignExpr)
    def printTree(self, indent=0):
        print("|  " * indent + self.type)
        self.id.printTree(indent + 1)
        self.value.printTree(indent + 1)

    @addToClass(AST.ForLoop)
    def printTree(self, indent=0):
        print("|  " * indent + "FOR")
        self.id.printTree(indent + 1)
        self.range.printTree(indent + 1)
        self.stmt.printTree(indent + 1)
    
    @addToClass(AST.Func)
    def printTree(self, indent=0):
        print("|  " * indent + "FUNC")
        self.id.printTree(indent + 1)
        for param in self.params:
            if hasattr(param, 'printTree'):
                param.printTree(indent + 1)
        self.body.printTree(indent + 1)


    @addToClass(AST.UntilLoop)
    def printTree(self, indent=0):
        print("|  " * indent + "UNTIL")
        self.cond.printTree(indent + 1)
        self.stmt.printTree(indent + 1)

    @addToClass(AST.Range)
    def printTree(self, indent=0):
        print("|  " * indent + "RANGE")
        self.min.printTree(indent + 1)
        self.max.printTree(indent + 1)

    @addToClass(AST.IfStmt)
    def printTree(self, indent=0):
        print("|  " * indent + "IFF")
        self.cond.printTree(indent + 1)
        print("|  " * indent + "THEN")
        self.positive.printTree(indent + 1)
        if self.negative:
            print("|  " * indent + "ELSE")
            self.negative.printTree(indent + 1)

    @addToClass(AST.Vector)
    def printTree(self, indent=0):
        print("|  " * indent + "VECTOR")
        for v in self.values:
            v.printTree(indent + 1)

    @addToClass(AST.Ref)
    def printTree(self, indent=0):
        print("|  " * indent + "REF")
        self.target.printTree(indent + 1)
        for i in self.indices:
            i.printTree(indent + 1)

    @addToClass(AST.Return)
    def printTree(self, indent=0):
        print("|  " * indent + "RETURN")
        self.expr.printTree(indent + 1)

    @addToClass(AST.Stop)
    def printTree(self, indent=0):
        print("|  " * indent + "BREAK")

    @addToClass(AST.Skip)
    def printTree(self, indent=0):
        print("|  " * indent + "STOP")

    @addToClass(AST.Error)
    def printTree(self, indent=0):
        print("| " * indent + "AAA")



