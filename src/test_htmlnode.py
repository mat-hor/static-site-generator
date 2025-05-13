import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_repr(self):
        node = HTMLNode("p","Test inside paragraph", [], {
        "href": "https://www.google.com",
        "target": "_blank",
        })
        self.assertEqual(repr(node), f"HTMLNode({node.tag}, {node.value}, {node.children}, {node.props})")
    
    def test_to_html_exception(self):
        node = HTMLNode()
        self.assertRaises(NotImplementedError, 
        node.to_html)

    def test_props_to_html(self):
        node = HTMLNode(props={
        "href": "https://www.google.com",
        "target": "_blank",
        })
        test_str = f' href="https://www.google.com" target="_blank"'
        self.assertEqual(node.props_to_html(), test_str)


if __name__ == "__main__":
    unittest.main()
