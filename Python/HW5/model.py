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

    def visit(self, visitor):
        return visitor.visit_number(self)


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

    def visit(self, visitor):
        return visitor.visit_function_definition(self)


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

    def visit(self, visitor):
        return visitor.visit_function_call(self)


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

    def visit(self, visitor):
        return visitor.visit_conditional(self)


class Print:
    def __init__(self, expr):
        self.expression = expr

    def evaluate(self, scope):
        res = self.expression.evaluate(scope)
        print(res.number)
        return res

    def visit(self, visitor):
        return visitor.visit_print(self)


class Read:
    def __init__(self, name):
        self.name = name

    def evaluate(self, scope):
        res = int(input())
        scope[self.name] = Number(res)
        return Number(res)

    def visit(self, visitor):
        return visitor.visit_read(self)


class Reference:
    def __init__(self, name):
        self.name = name

    def evaluate(self, scope):
        return scope[self.name]

    def visit(self, visitor):
        return visitor.visit_reference(self)


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

    def visit(self, visitor):
        return visitor.visit_binary_operation(self)


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

    def visit(self, visitor):
        return visitor.visit_unary_operation(self)


