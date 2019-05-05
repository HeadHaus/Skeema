import copy


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

    @property
    def parameters(self):
        return [parameter_node() for parameter_node in self._parameter_nodes]

    def __len__(self):
        return len(self._parameter_nodes)

    def __str__(self):
        return ', '.join((n() for n in self._parameter_nodes))


class SignatureNode(Node):
    def __init__(self, name: str, parameter_list_node: ParameterListNode):
        self._name = name
        self._parameter_list_node = parameter_list_node

    @property
    def name(self):
        return self._name

    def insert(self, index: int, parameter_node: ParameterNode):
        self._parameter_list_node.insert(index, parameter_node)

    @property
    def parameters(self):
        return self._parameter_list_node.parameters

    def __str__(self):
        return f'def {self._name}({self._parameter_list_node()}):\n'


class FunctionNode(Node):
    def __init__(self, signature_node: SignatureNode, body_nodes: [Node]):
        self._signature_node = copy.deepcopy(signature_node)
        if not body_nodes:
            body_nodes = [PassNode()]
        self._body_nodes = copy.deepcopy(body_nodes)

    @property
    def name(self):
        return self._signature_node.name

    @property
    def signature_node(self):
        return self._signature_node

    def __str__(self):
        body_lines = [f'\t{n()}' for n in self._body_nodes]
        body = '\n'.join(body_lines)
        return f'{self._signature_node()}{body}'


class MethodNode(FunctionNode):
    def __init__(self, signature_node: SignatureNode, body_nodes: [Node]):
        super().__init__(signature_node, body_nodes)
        self_node = ParameterNode('self')
        self.signature_node.insert(0, self_node)


class ClassMethodNode(FunctionNode):
    def __init__(self, signature_node: SignatureNode, body_nodes: [Node]):
        super().__init__(signature_node, body_nodes)
        cls_node = ParameterNode('cls')
        self.signature_node.insert(0, cls_node)


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


class ReturnNode(Node):
    def __init__(self, value_node: ValueNode):
        self._value_node = value_node

    def __str__(self):
        return f'return {self._value_node}'
