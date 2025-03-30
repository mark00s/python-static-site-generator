import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is some anchor text", TextType.NORMAL)
        self.assertEqual(repr(node), "TextNode(This is some anchor text, normal, None)")

    def test_link_repr(self):
        link_node = TextNode("This is some anchor text", TextType.LINK, "https://www.google.com")

        self.assertEqual(repr(link_node), "TextNode(This is some anchor text, link, https://www.google.com)")

    def test_non_url(self):
        node = TextNode("This is a text node", TextType.BOLD)

        self.assertEqual(node.url, None)

if __name__ == "__main__":
    unittest.main()
