def to_camel_case(snake):
    components = snake.split('_')
    components = (c.replace(c[0], c[0].upper(), 1) for c in components)
    return ''.join(components)
