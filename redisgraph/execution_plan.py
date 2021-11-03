class ExecutionPlan:
    def __init__(self, plan):
        self.plan = plan

    def __str__(self) -> str:
        return "\n".join(self.plan)

    def operation_tree(self):
        stack = []
        level = 0
        current = None
        i = 0
        while i < len(self.plan):
            op = self.plan[i]
            op_level = op.count("    ")
            if op_level == level:
                current = {"op": op.replace("    ", "")}
                i += 1
            elif op_level == level + 1:
                child = {"op": op.replace("    ", "")}
                if "children" not in current:
                    current["children"] = []
                current["children"].append(child)
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
