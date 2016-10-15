import yat.model as model


class ConstantFolder:
    def visit(self, tree):
        tree = tree.visit(self)
        return tree

    def visit_number(self, num):
        return num

    def visit_binary_operation(self, bin_op):
        bin_op.lhs = self.visit(bin_op.lhs)
        bin_op.rhs = self.visit(bin_op.rhs)

        if (bin_op.op == '*' and (isinstance(bin_op.lhs, model.Number) and bin_op.lhs.number == 0 and
                                  isinstance(bin_op.rhs, model.Reference) or
                                  isinstance(bin_op.rhs, model.Number) and bin_op.rhs.number == 0 and
                                  isinstance(bin_op.lhs, model.Reference))) or \
           (isinstance(bin_op.lhs, model.Reference) and isinstance(bin_op.rhs, model.Reference) and bin_op.op == '-' and
               bin_op.lhs.name == bin_op.rhs.name):
            return model.Number(0)
        if isinstance(bin_op.lhs, model.Number) and isinstance(bin_op.rhs, model.Number):
            return model.Number(bin_op.operations[bin_op.op](bin_op.lhs.number, bin_op.rhs.number))
        return bin_op

    def visit_unary_operation(self, un_op):
        while not isinstance(un_op.expression, model.Number):
            un_op.expression = self.visit(un_op.expression)
        return model.Number(un_op.operations[un_op.op](un_op.expression.number))

    def visit_reference(self, ref):
        return ref

    def visit_conditional(self, cond):
        cond.condition = cond.condition.visit(self)
        block = cond.if_true or []
        for i in range(len(block)):
            block[i] = self.visit(block[i])
        block = cond.if_false or []
        for i in range(len(block)):
            block[i] = self.visit(block[i])
        return cond

    def visit_print(self, prnt):
        return prnt.expression.visit(self)

    def visit_read(self, rd):
        return rd

    def visit_function_definition(self, func_def):
        for i in range(len(func_def.function.body)):
            func_def.function.body[i] = self.visit(func_def.function.body[i])
        return func_def

    def visit_function_call(self, func_call):
        for i in range(len(func_call.args)):
            func_call.args[i] = self.visit(func_call.args[i])
        func_call.fun_expr = func_call.fun_expr.visit(self)
        return func_call
