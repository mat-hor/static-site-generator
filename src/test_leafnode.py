import unittest
from leafnode import LeafNode

class TestLeaftNode(unittest.TestCase):

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_to_html_empty_value(self):
        node = LeafNode("p", None)
        self.assertRaises(ValueError, node.to_html)

    def test_to_html_empty_tag(self):
        node = LeafNode(None, "AAA")
        self.assertEqual(node.value, node.to_html())


if __name__ == "__main__":
    unittest.main()
