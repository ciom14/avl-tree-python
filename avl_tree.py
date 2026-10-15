import sys


class Node:
    """Вершина AVL-дерева."""

    def __init__(self, key: int) -> None:
        self.key: int = key
        self.left: Node | None = None
        self.right: Node | None = None
        self.height: int = 1


def get_height(node: Node | None) -> int:
    """Возвращает высоту вершины, для пустой (None) это 0."""
    # без этой проверки падаем на None
    return node.height if node else 0


def update(node: Node) -> None:
    """Пересчитывает высоту вершины по высотам её детей."""
    node.height = 1 + max(get_height(node.left), get_height(node.right))


def get_balance(node: Node) -> int:
    """Возвращает баланс: высота правого минус высота левого."""
    return get_height(node.right) - get_height(node.left)


def rotate_left(a: Node) -> Node:
    """Левый поворот вокруг a, возвращает новый корень поддерева."""
    b = a.right
    a.right = b.left
    b.left = a
    update(a)
    update(b)
    return b


def rotate_right(a: Node) -> Node:
    """Правый поворот вокруг a, возвращает новый корень поддерева."""
    b = a.left
    a.left = b.right
    b.right = a
    update(a)
    update(b)
    return b


def balance(node: Node) -> Node:
    """Обновляет высоту и балансирует вершину, если |баланс| == 2.

    Возвращает корень поддерева после балансировки.
    """
    update(node)
    bal = get_balance(node)
    if bal == 2:
        # правое слишком тяжёлое
        if get_balance(node.right) < 0:
            node.right = rotate_right(node.right)
        return rotate_left(node)
    if bal == -2:
        # тут всё зеркально
        if get_balance(node.left) > 0:
            node.left = rotate_left(node.left)
        return rotate_right(node)
    return node


def add(node: Node | None, key: int) -> Node:
    """Вставляет ключ в поддерево, возвращает новый корень поддерева.

    Если ключ уже есть, дерево не меняется.
    """
    if node is None:
        return Node(key)
    if key < node.key:
        node.left = add(node.left, key)
    elif key > node.key:
        node.right = add(node.right, key)
    else:
        return node
    return balance(node)


def delete_min(node: Node) -> Node | None:
    """Удаляет минимальную вершину поддерева.

    Возвращает новый корень поддерева (с балансировкой по пути).
    """
    # выкидываем самую левую вершину
    if node.left is None:
        return node.right
    node.left = delete_min(node.left)
    # балансим на обратном пути, как в условии
    return balance(node)


def delete(node: Node | None, key: int) -> Node | None:
    """Удаляет ключ из поддерева, возвращает новый корень поддерева.

    Если ключа нет, ничего не происходит.
    """
    if node is None:
        return None
    if key < node.key:
        node.left = delete(node.left, key)
    elif key > node.key:
        node.right = delete(node.right, key)
    else:
        if node.left is None:
            return node.right
        if node.right is None:
            return node.left
        min_node = node.right
        while min_node.left:
            min_node = min_node.left
        node.key = min_node.key
        node.right = delete_min(node.right)
    return balance(node)


def exists(node: Node | None, key: int) -> bool:
    """Проверяет, есть ли ключ в дереве."""
    while node:
        if key == node.key:
            return True
        node = node.left if key < node.key else node.right
    return False


def find_next(node: Node | None, key: int) -> int | None:
    """Ищет минимальный ключ >= key, если такого нет, то None."""
    result = None
    while node:
        if node.key >= key:
            result = node.key
            node = node.left
        else:
            node = node.right
    return result


def find_prev(node: Node | None, key: int) -> int | None:
    """Ищет максимальный ключ <= key, если такого нет, то None."""
    result = None
    while node:
        if node.key <= key:
            result = node.key
            node = node.right
        else:
            node = node.left
    return result


def preorder(root: Node) -> list[int]:
    """Возвращает ключи дерева в порядке прямого обхода."""
    result = []
    stack = [root]
    while stack:
        node = stack.pop()
        result.append(node.key)
        # правого кладём первым, чтобы левый вышел раньше
        if node.right:
            stack.append(node.right)
        if node.left:
            stack.append(node.left)
    return result


def main() -> None:
    """Читает команды из stdin и выводит ответы на запросы."""
    data = sys.stdin.read().split()
    q = int(data[0])
    pos = 1
    root: Node | None = None
    output: list[str] = []

    for _ in range(q):
        cmd = data[pos]
        pos += 1

        if cmd == "add":
            root = add(root, int(data[pos]))
            pos += 1
        elif cmd == "del":
            root = delete(root, int(data[pos]))
            pos += 1
        elif cmd == "exists":
            found = exists(root, int(data[pos]))
            output.append("YES" if found else "NO")
            pos += 1
        elif cmd == "next":
            value = find_next(root, int(data[pos]))
            output.append("None" if value is None else str(value))
            pos += 1
        elif cmd == "prev":
            value = find_prev(root, int(data[pos]))
            output.append("None" if value is None else str(value))
            pos += 1
        elif cmd == "root":
            output.append(str(root.key) if root else "Empty")
        elif cmd == "height":
            output.append(str(get_height(root)))
        elif cmd == "print":
            if root is None:
                output.append("Empty")
            else:
                output.append(" ".join(map(str, preorder(root))))

    print("\n".join(output))


if __name__ == "__main__":
    main()