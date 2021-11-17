class Operation:
    def __init__(self, name, args=None):
        self.name = name
        self.args = args
        self.children = []

    def append_child(self, child):
        self.children.append(child)
        return self

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, Operation):
            return False
        
        if self.name != o.name or self.args != self.args or len(self.children) != len(o.children):
            return False

        for i in range(len(self.children)):
            if not self.children[i] == o.children[i]:
                return False
        
        return True


class ExecutionPlan:
    def __init__(self, plan):
        self.plan = plan
        self.structured_plan = self._operation_tree()

    def __str__(self) -> str:
        return "\n".join(self.plan)

    def _operation_tree(self):
        i       = 0
        level   = 0
        stack   = []
        current = None

        while i < len(self.plan):
            op = self.plan[i]
            op_level = op.count("    ")
            if op_level == level:
                args = op.split("|")
                current = Operation(args[0].strip(), None if len(args) == 1 else args[1].strip())
                i += 1
            elif op_level == level + 1:
                args = op.split("|")
                child = Operation(args[0].strip(), None if len(args) == 1 else args[1].strip())
                current.children.append(child)
                stack.append(current)
                current = child
                level += 1
                i += 1
            elif op_level < level:
                levels_back = level - op_level + 1
                for _ in range(levels_back):
                    current = stack.pop()
                level -= levels_back
            else:
                raise Exception("corrupted plan")
        return stack[0]
