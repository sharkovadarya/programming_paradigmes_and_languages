import yat.model as model


class ConstantFolder:
    def visit(self, tree):
        new_tree = tree.visit(self)
        return new_tree

    def process_list(self, lst):
        ret_lst = []
        for action in lst:
            ret_lst.append(self.visit(action))
        return ret_lst

    def visit_number(self, num):
        return num

    def visit_binary_operation(self, bin_op):
        lhs = self.visit(bin_op.lhs)
        rhs = self.visit(bin_op.rhs)

        if (bin_op.op == '*' and (isinstance(lhs, model.Number) and lhs.number == 0 and
                                  isinstance(rhs, model.Reference) or
                                  isinstance(rhs, model.Number) and rhs.number == 0 and
                                  isinstance(lhs, model.Reference))) or \
           (isinstance(lhs, model.Reference) and isinstance(rhs, model.Reference) and bin_op.op == '-' and
               lhs.name == rhs.name):
            return model.Number(0)
        if isinstance(lhs, model.Number) and isinstance(rhs, model.Number):
            return model.Number(bin_op.operations[bin_op.op](lhs.number, rhs.number))
        return model.BinaryOperation(lhs, bin_op.op, rhs)

    def visit_unary_operation(self, un_op):
        ex = self.visit(un_op.expression)
        if isinstance(ex, model.Number):
            return model.Number(un_op.operations[un_op.op](ex.number))
        return model.UnaryOperation(un_op.op, ex)

    def visit_reference(self, ref):
        return ref

    def visit_conditional(self, cond):
        condition = cond.condition.visit(self)
        if_true = self.process_list(cond.if_true or [])
        if_false = self.process_list(cond.if_false or [])
        return model.Conditional(condition, if_true, if_false)

    def visit_print(self, prnt):
        return model.Print(prnt.expression.visit(self))

    def visit_read(self, rd):
        return rd

    def visit_function_definition(self, func_def):
        body = self.process_list(func_def.function.body)
        return model.FunctionDefinition(func_def.name, model.Function(func_def.function.args, body))

    def visit_function_call(self, func_call):
        args = self.process_list(func_call.args)
        fun_expr = func_call.fun_expr.visit(self)
        return model.FunctionCall(fun_expr, args)
