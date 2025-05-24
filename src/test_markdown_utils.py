import unittest
from markdown_utils import extract_markdown_images, extract_markdown_links, markdown_to_blocks, block_to_block_type

class TestMarkdownUtils(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
        "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual([('to boot dev', 'https://www.boot.dev'), ('to youtube', 'https://www.youtube.com/@bootdotdev')], matches)


    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_block_to_block_type(self):
        md = """
# Heading 1

## Heading 2

### Heading 3

#### Heading 4

##### Heading 5

###### Heading 6

This is a paragraph of text.

This is a **bold** word.

This is an _italic_ word.

This is a paragraph with a [link](https://www.google.com).

- Item 1
- Item 2
- Item 3

1. Item 1
2. Item 2
3. Item 3

```
This is code
```
"""
        result = []
        blocks = markdown_to_blocks(md)
        for block in blocks:
            result.append(block_to_block_type(block).value)
        self.assertEqual(
            result,
            ['heading', 'heading', 'heading', 'heading', 'heading', 'heading', 'paragraph', 'paragraph', 'paragraph', 'paragraph', 'unordered_list', 'ordered_list', 'paragraph'],
        )

        
