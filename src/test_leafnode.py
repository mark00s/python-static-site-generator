import unittest

from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_no_props(self):
        leaf = LeafNode("p", "This is a paragraph of text.")

        self.assertEqual(leaf.to_html(), "<p>This is a paragraph of text.</p>")

    def test_node(self):
        leaf = LeafNode("a", "Click me!", {"href": "https://www.google.com"})

        self.assertEqual(
            leaf.to_html(), '<a href="https://www.google.com">Click me!</a>'
        )

    def test_no_value_to_html(self):
        leaf = LeafNode("p", None)

        with self.assertRaises(ValueError):
            leaf.to_html()

    def test_no_tag_to_html(self):
        text = "Some Text"
        leaf = LeafNode(None, text)

        self.assertEqual(leaf.to_html(), text)
