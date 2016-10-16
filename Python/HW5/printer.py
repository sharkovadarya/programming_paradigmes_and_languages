class PrettyPrinter:
    def __init__(self):
        self.padding = 0

    def visit(self, tree):
        print(self.padding * " ", end="")
        tree.visit(self)
        print(";")

    def process_list(self, lst):
        self.padding += 4
        for action in lst:
            self.visit(action)
        self.padding -= 4

    def visit_number(self, num):
        print("(", end="")
        print(str(num.number) , end="")
        print(")", end="")

    def visit_conditional(self, conditional):
        print("if (", end="")
        conditional.condition.visit(self)
        print(") {")

        self.process_list(conditional.if_true or [])
        print(self.padding * " " + "} else {")
        self.process_list(conditional.if_false or [])
        print(self.padding * " " + "}", end="")

    def visit_reference(self, ref):
        print(ref.name, end='')

    def visit_binary_operation(self, bin_op):
        print('(', end='')
        bin_op.lhs.visit(self)
        print(bin_op.op, end='')
        bin_op.rhs.visit(self)
        print(')', end='')

    def visit_unary_operation(self, un_op):
        print('({}'.format(un_op.op), end='')
        un_op.expression.visit(self)
        print(')', end='')

    def visit_print(self, prnt):
        print("print", end=" ")
        prnt.expression.visit(self)

    def visit_read(self, rd):
        print("read", rd.name, end="")

    def visit_function_definition(self, func_def):
        print("def", func_def.name, end="(")
        print(','.join(func_def.function.args), end="")
        print(") {")
        self.process_list(func_def.function.body)
        print(self.padding * " " + "}", end="")

    def visit_function_call(self, func_call):
        func_call.fun_expr.visit(self)
        print("(", end="")
        if len(func_call.args):
            for arg in func_call.args[:-1]:
                arg.visit(self)
                print(",", end="")
            func_call.args[-1].visit(self)
        print(")", end="")
