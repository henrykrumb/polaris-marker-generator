def cylinder(h, r1, r2=0, fn=40):
    def _inner(indent=0):
        nonlocal h
        nonlocal r1
        nonlocal r2
        if r2 == 0:
            r2 = r1
        return '  ' * indent + f'cylinder(h={h}, r1={r1}, r2={r2}, $fn={fn});'
    return _inner


def cube(x, y, z):
    def _inner(indent=0):
        nonlocal x
        nonlocal y
        nonlocal z
        return '  ' * indent + f'cube([{x:.4f}, {y:.4f}, {z:.4f}]);'
    return _inner


def __iterate_children(children, indent):
    text = '{\n'
    for child in children:
        text += f'{child(indent + 1)}\n'
    text += '  ' * indent + '}'
    return text


def hull(children):
    def _inner(indent=0):
        nonlocal children
        text = '  ' * indent + 'hull()'
        return text + ' ' + __iterate_children(children, indent)
    return _inner


def union(children):
    def _inner(indent=0):
        nonlocal children
        text = '  ' * indent + 'union()'
        return text + ' ' + __iterate_children(children, indent)
    return _inner


def translate(x, y, z, children):
    def _inner(indent=0):
        nonlocal x
        nonlocal y
        nonlocal z
        nonlocal children
        text = '  ' * indent + f'translate([{x:.4f}, {y:.4f}, {z:.4f}])'
        return text + ' ' + __iterate_children(children, indent)
    return _inner


def rotate(x, y, z, children):
    def _inner(indent=0):
        nonlocal x
        nonlocal y
        nonlocal z
        nonlocal children
        text = '  ' * indent + f'rotate([{x:.4f}, {y:.4f}, {z:.4f}])'
        return text + ' ' + __iterate_children(children, indent)
    return _inner


def chamfered_cylinder(h, r, chamfer=0.5):
    def _inner(indent=0):
        nonlocal h
        nonlocal r
        nonlocal chamfer
        return union([
            cylinder(h - chamfer, r),
            translate(0, 0, h - chamfer, [
                cylinder(chamfer, r1=r, r2=r - chamfer)
            ])
        ])(indent)
    return _inner
