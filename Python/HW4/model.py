class Scope(object):
    def __init__(self, parent=None):
        self.parent = parent
        self.dictionary = {}

    def __getitem__(self, item):
        dct = self.dictionary
        if item not in self.dictionary:
            return self.parent[item]
        return self.dictionary[item]

    def __setitem__(self, key, value):
        self.dictionary[key] = value


class Number:
    number = 0

    def __init__(self, value):
        self.number = value

    def evaluate(self, scope):
        return self

    def __add__(self, other):
        return Number(self.number + other.number)

    def __sub__(self, other):
        return Number(self.number - other.number)

    def __mul__(self, other):
        return Number(self.number * other.number)

    def __truediv__(self, other):
        return Number(self.number / other.number)

    def __mod__(self, other):
        return Number(self.number % other.number)

    def __eq__(self, other):
        if self.number == other.number:
            return Number(1)
        return Number(0)

    def __ne__(self, other):
        if self.number != other.number:
            return Number(1)
        return Number(0)

    def __le__(self, other):
        if self.number <= other.number:
            return Number(1)
        return Number(0)

    def __ge__(self, other):
        if self.number >= other.number:
            return Number(1)
        return Number(0)

    def __lt__(self, other):
        if self.number < other.number:
            return Number(1)
        return Number(0)

    def __gt__(self, other):
        if self.number > other.number:
            return Number(1)
        return Number(0)

    def __and__(self, other):
        if self.number and other.number:
            return Number(1)
        return Number(0)

    def __or__(self, other):
        if self.number or other.number:
            return Number(1)
        return Number(0)

    def __neg__(self):
        return Number(-self.number)

    def __not__(self):
        if self.number:
            return Number(0)
        return Number(1)


class Function:
    def __init__(self, args, body):
        self.args = args
        self.body = body
        self.res = 0

    def evaluate(self, scope):
        for expr in self.body:
            self.res = expr.evaluate(scope)
        return self.res


class FunctionDefinition:
    def __init__(self, name, function):
        self.name = name
        self.function = function

    def evaluate(self, scope):
        scope[self.name] = self.function
        return self.function


# important: source said condtion
class Conditional:
    def __init__(self, condition, if_true, if_false=None):
        self.condition = condition
        self.if_true = if_true
        self.if_false = if_false

    def evaluate(self, scope):
        num = self.condition.evaluate(scope)
        res = Number(0)
        if num.number == 0:
            for expr in self.if_false:
                res = expr.evaluate(scope)
            return res
        for expr in self.if_true:
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
        scope[self.name] = res
        return Number(res)


class FunctionCall:
    def __init__(self, fun_expr, args):
        self.fun_expr = fun_expr
        self.args = args

    def evaluate(self, scope):
        call_scope = Scope(scope)
        for arg, name in self.args, self.fun_expr.evaluate(scope).args:
            call_scope[name] = arg.evaluate(call_scope)
        function = Function(self.args, call_scope)
        return function.evaluate(call_scope)


class Reference:
    def __init__(self, name):
        self.name = name

    def evaluate(self, scope):
        return scope[self.name]


class BinaryOperation:
    def __init__(self, lhs, op, rhs):
        self.lhs = lhs
        self.op = op
        self.rhs = rhs

    def evaluate(self, scope):
        if self.op == '+':
            return self.lhs.evaluate(scope) + self.rhs.evaluate(scope)
        if self.op == '-':
            return self.lhs.evaluate(scope) - self.rhs.evaluate(scope)
        if self.op == '*':
            return self.lhs.evaluate(scope) * self.rhs.evaluate(scope)
        if self.op == '/':
            return self.lhs.evaluate(scope) / self.rhs.evaluate(scope)
        if self.op == '%':
            return self.lhs.evaluate(scope) % self.rhs.evaluate(scope)
        if self.op == '==':
            return self.lhs.evaluate(scope) == self.rhs.evaluate(scope)
        if self.op == '!=':
            return self.lhs.evaluate(scope) != self.rhs.evaluate(scope)
        if self.op == '>':
            return self.lhs.evaluate(scope) > self.rhs.evaluate(scope)
        if self.op == '>=':
            return self.lhs.evaluate(scope) >= self.rhs.evaluate(scope)
        if self.op == '<':
            return self.lhs.evaluate(scope) < self.rhs.evaluate(scope)
        if self.op == '<=':
            return self.lhs.evaluate(scope) <= self.rhs.evaluate(scope)
        if self.op == '&&':
            return self.lhs.evaluate(scope) and self.rhs.evaluate(scope)
        if self.op == '||':
            return self.lhs.evaluate(scope) or self.rhs.evaluate(scope)


class UnaryOperation:
    def __init__(self, op, expr):
        self.op = op
        self.expression = expr

    def evaluate(self, scope):
        if self.op == '-':
            return -self.expression.evaluate(scope)
        if self.op == '!':
            return self.expression.evaluate(scope).__not__()

if __name__ == '__main__':
    # testing: Scope, Number
    parent = Scope()
    parent['bar'] = Number(10)
    num = Number(5)

    # testing: Function, Scope
    parent["foo"] = Function(num, num + Number(2))
    scope = Scope(parent)
    ans = scope["bar"]
    scope["bar"] = Number(20)
    ans = scope["bar"]  # ans == Number(20)
    ans = scope["foo"]  # ans == Function(...)

    # testing: Read
    rd = Read("nmb")
    x = rd.evaluate(scope)

    # testing: Function, FunctionDefinition, Conditional
    func = Function(num, num * Number(2))
    func_def = FunctionDefinition("multiply_by_two", func)
    cons = Conditional(num > Number(5), None, [num - Number(1)])
    cond = Conditional(num + Number(1) == Number(6), [num % Number(4)], [num + Number(17)])

    # testing: Print
    prnt = Print(cons)
    m = prnt.evaluate(scope)
    prnt = Print(cond)
    k = prnt.evaluate(scope)

    # testing: FunctionCall
    f = FunctionCall(func_def, [Number(2)])

    # testing: BinaryOperation
    bin_op = BinaryOperation(k, "%", m)
    prnt = Print(bin_op)
    prnt.evaluate(scope)

    # testing: UnaryOperation
    un_op = UnaryOperation("!", Number(0))
    prnt = Print(un_op)
    prnt.evaluate(scope)

    # testing: reference
    ref = Reference("bar")
    o = ref.evaluate(scope)
    prnt = Print(o)
    prnt.evaluate(scope)