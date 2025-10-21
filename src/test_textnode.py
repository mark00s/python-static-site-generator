import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_false_tt(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_eq_false_value(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        node2 = TextNode("This is a text node2", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_eq_url(self):
        node = TextNode(
            "This is a text node", TextType.ITALIC, "https://www.google.com"
        )
        node2 = TextNode(
            "This is a text node", TextType.ITALIC, "https://www.google.com"
        )
        self.assertEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is some anchor text", TextType.TEXT)
        self.assertEqual(repr(node), "TextNode(This is some anchor text, text, None)")

    def test_link_repr(self):
        link_node = TextNode(
            "This is some anchor text", TextType.LINK, "https://www.google.com"
        )

        self.assertEqual(
            repr(link_node),
            "TextNode(This is some anchor text, link, https://www.google.com)",
        )

    def test_non_url(self):
        node = TextNode("This is a text node", TextType.BOLD)

        self.assertEqual(node.url, None)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_image(self):
        node = TextNode("This is an image", TextType.IMAGE, "https://www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {"src": "https://www.boot.dev", "alt": "This is an image"},
        )

    def test_bold(self):
        node = TextNode("This is bold", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is bold")


if __name__ == "__main__":
    unittest.main()
