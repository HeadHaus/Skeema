class Node:
    def __call__(self):
        return str(self)


class ParameterNode(Node):
    def __init__(self, name: str, klass: str = None):
        self._name = name
        self._klass = klass

    def __str__(self):
        if self._klass:
            return f'{self._name}: {self._klass}'
        else:
            return f'{self._name}'


class ParameterListNode(Node):
    def __init__(self, parameter_nodes: [ParameterNode]):
        self._parameter_nodes = parameter_nodes

    def insert(self, index: int, parameter_node: ParameterNode):
        self._parameter_nodes.insert(index, parameter_node)

    def __str__(self):
        return ', '.join((n() for n in self._parameter_nodes))


class SignatureNode(Node):
    def __init__(self, name: str, parameter_list_node: ParameterListNode):
        self._name = name
        self._parameter_list_node = parameter_list_node

    def insert(self, index: int, parameter_node: ParameterNode):
        self._parameter_list_node.insert(index, parameter_node)

    def __str__(self):
        return f'def {self._name}({self._parameter_list_node()}):\n'


class MethodNode(Node):
    def __init__(self, signature_node: SignatureNode, body_nodes: [Node]):
        self_node = ParameterNode('self')
        signature_node.insert(0, self_node)
        self._signature_node = signature_node
        if not body_nodes:
            body_nodes = [PassNode()]
        self._body_nodes = body_nodes

    def __str__(self):
        body_lines = [f'\t{n()}' for n in self._body_nodes]
        body = '\n'.join(body_lines)
        return f'{self._signature_node()}{body}'


class ValueNode(Node):
    def __init__(self, value: str):
        self._value = value

    def __str__(self):
        return self._value


class PassNode(Node):
    def __str__(self):
        return 'pass\n'


class AssignmentNode(Node):
    def __init__(self, lhs: ValueNode, rhs: ValueNode):
        self._lhs = lhs
        self._rhs = rhs

    def __str__(self):
        return f'{self._lhs} = {self._rhs}'
