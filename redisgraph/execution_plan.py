class Operation:
    """
    Operation, single operation within execution plan.
    """

    def __init__(self, name, args=None):
        """
        Create a new operation.

        Args:
            name: string that represents the name of the operation
            args: operation arguments
        """
        self.name = name
        self.args = args
        self.children = []

    def append_child(self, child):
        if not isinstance(child, Operation) or self is child:
            raise Exception("child must be Operation")

        self.children.append(child)
        return self

    def child_count(self):
        return len(self.children)

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, Operation):
            return False

        if self.name != o.name or self.args != o.args:
            return False

        return True

    def __str__(self) -> str:
        args_str = "" if self.args is None else f" | {self.args}"
        return f"{self.name}{args_str}"


class ExecutionPlan:
    """
    ExecutionPlan, collection of operations.
    """

    def __init__(self, plan):
        """
        Create a new execution plan.

        Args:
            plan: array of strings that represents the collection operations
                  the output from GRAPH.EXPLAIN
        """
        if not isinstance(plan, list):
            raise Exception("plan must be an array")

        self.plan = plan
        self.structured_plan = self._operation_tree()

    def _compare_operations(self, root_a, root_b):
        """
            Compare execution plan operation tree

            Return: True if operation trees are equal, False otherwise
        """

        # compare current root
        if root_a != root_b:
            return False

        # make sure root have the same number of children
        if root_a.child_count() != root_b.child_count():
            return False

        # recursively compare children
        for i in range(root_a.child_count()):
            if not self._compare_operations(root_a.children[i], root_b.children[i]):
                return False

        return True

    def __str__(self) -> str:
        def aggraget_str(str_children):
            return "\n".join(["    " + line for str_child in str_children for line in str_child.splitlines()])

        def combine_str(x, y):
            return f"{x}\n{y}"

        return self._operation_traverse(self.structured_plan, str, aggraget_str, combine_str)

    def __eq__(self, o: object) -> bool:
        """ Compares two execution plans

            Return: True if the two plans are equal False otherwise
        """
        # make sure 'o' is an execution-plan
        if not isinstance(o, ExecutionPlan):
            return False

        # get root for both plans
        root_a = self.structured_plan
        root_b = o.structured_plan

        # compare execution trees
        return self._compare_operations(root_a, root_b)

    def _operation_traverse(self, op, op_f, aggregate_f, combine_f):
        """
        Traverse operation tree recursively applying functions

        Args:
            op: operation to traverse
            op_f: function applied for each operation
            aggregate_f: aggregation function applied for all children of a single operation
            combine_f: combine function applied for the operation result and the children result
        """
        # apply op_f for each operation
        op_res = op_f(op)
        if len(op.children) == 0:
            return op_res  # no children return
        else:
            # apply _operation_traverse recursively
            children = [self._operation_traverse(child, op_f, aggregate_f, combine_f) for child in op.children]
            # combine the operation result with the children aggregated result
            return combine_f(op_res, aggregate_f(children))

    def _operation_tree(self):
        """ Build the operation tree from the string representation """

        # initial state
        i = 0
        level = 0
        stack = []
        current = None

        # iterate plan operations
        while i < len(self.plan):
            current_op = self.plan[i]
            op_level = current_op.count("    ")
            if op_level == level:
                # if the operation level equal to the current level
                # set the current operation and move next
                args = current_op.split("|")
                current = Operation(args[0].strip(), None if len(args) == 1 else args[1].strip())
                i += 1
            elif op_level == level + 1:
                # if the operation is child of the current operation
                # add it as child and set as current operation
                args = current_op.split("|")
                child = Operation(args[0].strip(), None if len(args) == 1 else args[1].strip())
                current.append_child(child)
                stack.append(current)
                current = child
                level += 1
                i += 1
            elif op_level < level:
                # if the operation is not child of current operation
                # go back to it's parent operation
                levels_back = level - op_level + 1
                for _ in range(levels_back):
                    current = stack.pop()
                level -= levels_back
            else:
                raise Exception("corrupted plan")
        return stack[0]