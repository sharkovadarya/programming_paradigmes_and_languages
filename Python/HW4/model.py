class Scope(object):
    def __init__(self, parent=None):
        self.parent = parent
        self.dictionary = {}

    def __getitem__(self, item):
        if self.parent and item not in self.dictionary:
            return self.parent[item]
        return self.dictionary[item]

    def __setitem__(self, key, value):
        self.dictionary[key] = value


class Number:
    def __init__(self, value):
        self.number = value

    def evaluate(self, scope):
        return self


class Function:
    def __init__(self, args, body):
        self.args = args
        self.body = body

    def evaluate(self, scope):
        res = Number(0)
        for expr in self.body:
            res = expr.evaluate(scope)
        return res


class FunctionDefinition:
    def __init__(self, name, function):
        self.name = name
        self.function = function

    def evaluate(self, scope):
        scope[self.name] = self.function
        return self.function


class FunctionCall:
    def __init__(self, fun_expr, args):
        self.fun_expr = fun_expr
        self.args = args

    def evaluate(self, scope):
        function = self.fun_expr.evaluate(scope)
        call_scope = Scope(scope)
        i = 0
        for arg in self.args:
            call_scope[function.args[i]] = arg.evaluate(scope)
            i += 1
        scope = call_scope
        return function.evaluate(scope)


class Conditional:
    def __init__(self, condtion, if_true, if_false=None):
        self.condition = condtion
        self.if_true = if_true
        self.if_false = if_false

    def evaluate(self, scope):
        num = self.condition.evaluate(scope)
        if num.number == 0:
            block = self.if_false
        else:
            block = self.if_true
        res = Number(1)
        for expr in block or []:
            res = expr.evaluate(scope)
        return res


class Print:
    def __init__(self, expr):
        self.expression = expr

    def evaluate(self, scope):
        res = self.expression.evaluate(scope)
        print(res.number)
        return res


class Read:
    def __init__(self, name):
        self.name = name

    def evaluate(self, scope):
        res = int(input())
        scope[self.name] = Number(res)
        return Number(res)


class Reference:
    def __init__(self, name):
        self.name = name

    def evaluate(self, scope):
        return scope[self.name]


class BinaryOperation:
    operations = {'+': lambda x, y: x + y,
                  '-': lambda x, y: x - y,
                  '*': lambda x, y: x * y,
                  '/': lambda x, y: x // y,
                  '%': lambda x, y: x % y,
                  '==': lambda x, y: 1 if x == y else 0,
                  '!=': lambda x, y: 1 if x != y else 0,
                  '>': lambda x, y: 1 if x > y else 0,
                  '>=': lambda x, y: 1 if x >= y else 0,
                  '<': lambda x, y: 1 if x < y else 0,
                  '<=': lambda x, y: 1 if x <= y else 0,
                  '&&': lambda x, y: x and y,
                  '||': lambda x, y: x or y
                  }

    def __init__(self, lhs, op, rhs):
        self.lhs = lhs
        self.op = op
        self.rhs = rhs

    def evaluate(self, scope):
        return Number(self.operations[self.op](self.lhs.evaluate(scope).number, self.rhs.evaluate(scope).number))


class UnaryOperation:
    operations = {
        '-': lambda x: -x,
        '!': lambda x: 1 if not x else 0
    }

    def __init__(self, op, expr):
        self.op = op
        self.expression = expr

    def evaluate(self, scope):
        return Number(self.operations[self.op](self.expression.evaluate(scope).number))

if __name__ == '__main__':
    # testing: Scope, Number
    parent = Scope()
    parent["bar"] = Number(10)
    num = Number(5)
    scope = Scope(parent)
    scope["bar"] = Number(20)

    # testing: Read
    rd = Read("nmb")
    x = rd.evaluate(scope)

    # testing: Conditional
    cond1 = Conditional(BinaryOperation(num, '>', Number(5)), None, None)
    cond2 = Conditional(BinaryOperation(BinaryOperation(num, '+', Number(1)), '>', Number(6)),
                        [Print(Number(30))], [Print(Number(59))])

    # testing: Print
    prnt = Print(cond1)
    m = prnt.evaluate(scope)
    prnt = Print(cond2)
    k = prnt.evaluate(scope)

    # testing: BinaryOperation
    bin_op = BinaryOperation(k, "/", m)
    prnt = Print(bin_op)
    prnt.evaluate(scope)

    # testing: UnaryOperation
    un_op = UnaryOperation("!", Number(0))
    prnt = Print(un_op)
    prnt.evaluate(scope)
    Print(UnaryOperation('-', Number(3))).evaluate(scope)
    Print(BinaryOperation(Number(2), '||', Number(0))).evaluate(scope)

    # testing: reference
    ref = Reference("bar")
    o = ref.evaluate(scope)
    prnt = Print(o)
    v = prnt.evaluate(scope)    

    # testing: Function, FunctionDefinition, FunctionCall
    f = Function(["first", "second"], [BinaryOperation(Reference("first"), '*', Reference("second"))])
    fd = FunctionDefinition("multiply", f)
    res = FunctionCall(fd, [v, Number(3)])
    prnt = Print(res)
    l = prnt.evaluate(scope)

    g = Function(["x"], [Conditional(BinaryOperation(UnaryOperation('-', Reference("x")), '<=', Number(-7)),
                                     [Print(FunctionCall(fd, [Reference("x"), Number(5)]))],
                                     [Print(BinaryOperation(Reference("x"), "%", Number(2))),
                                      Print(FunctionCall(fd, [Reference("x"), m]))]),
                         FunctionCall(fd, [Reference("x"), Number(3)])])
    gd = FunctionDefinition("g", g)
    res = FunctionCall(gd, [Number(9)])
    prnt = Print(res)
    res = prnt.evaluate(scope)
    res = FunctionCall(gd, [Number(2)])
    prnt = Print(res)
    res = prnt.evaluate(scope)

    Conditional(Read("t").evaluate(scope), [Print(Number(1))], [Print(Number(0))]).evaluate(scope)
