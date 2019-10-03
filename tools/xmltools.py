import xml.etree.cElementTree as ET

__all__ = ['etree_find', 'etree_find_all', 'etree_contains']


def etree_find(root: ET.Element, tag: str, ignore_namespaces=False):
    """
    Returns the first xml.etree.cElementTree.Element with a matching tag
    in a depth-first traversal of the tree. Returns None if no Element
    with a matching tag is found.

    :param root: xml.etree.cElementTree root Element.
    :param tag: XML tag to match.
    :param ignore_namespaces: if True, also matches tags with
                            arbitrary namespace prefixes.
    :raises ValueError if root is None.
    """
    if root is None:
        raise ValueError("root must be non-null.")

    stack = [root]
    while stack:
        cur = stack.pop()
        # list(cur) yields all children of an ET.Element
        stack.extend(list(cur))

        cur_tag = cur.tag.split("}")[-1] if ignore_namespaces else cur.tag
        if tag == cur_tag:
            return cur
    return None


def etree_find_all(root: ET.Element, tag: str, ignore_namespaces=False):
    """
    Returns all xml.etree.cElementTree.Element objects with matching tags
    in the tree. Returns an empty list if no Element with a matching tag is found.

    :param root: xml.etree.cElementTree root Element.
    :param tag: XML tag to match.
    :param ignore_namespaces: if True, also matches tags with
                        arbitrary namespace prefixes.
    :raises ValueError if root is None.
    """
    if root is None:
        raise ValueError("root must be non-null.")

    stack, matches = [root], []
    while stack:
        cur = stack.pop()
        # list(cur) yields all children of an ET.Element
        stack.extend(list(cur))

        cur_tag = cur.tag.split("}")[-1] if ignore_namespaces else cur.tag
        if tag == cur_tag:
            matches.append(cur)
    return matches


def etree_contains(root: ET.Element, tag: str, ignore_namespaces=False):
    """
    Returns True if a xml.etree.cElementTree.Element with a matching tag
    exists in the tree with root 'root'. Returns False otherwise.

    Equivalent to (etree_find() is not None).

    :param root: xml.etree.cElementTree root Element.
    :param tag: XML tag to match.
    :param ignore_namespaces: if True, also matches tags with
                    arbitrary namespace prefixes.
    :raises ValueError if root is None.
    """
    return etree_find(root, tag, ignore_namespaces) is not None
