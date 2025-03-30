import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_to_html(self):
        node = HTMLNode()
        with self.assertRaises(NotImplementedError):  
            node.to_html()

    def test_props_to_html(self):
        node = HTMLNode(props={
            "href": "https://www.google.com",
            "target": "_blank",
        })
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')

    def test_non_string_props(self):
        node = HTMLNode(props={
            'XD': None,
            'easda': 23123
        })
        self.assertEqual(node.props_to_html(), ' XD="None" easda="23123"')
