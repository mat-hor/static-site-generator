import re
from enum import Enum

class BlockType(Enum):
    PARAGRAPG = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def extract_markdown_images(text):
    matches = re.findall(r"\!\[(.*?)\]\((.*?)\)", text)
    return matches


def extract_markdown_links(text):
    matches = re.findall(r"\[(.*?)\]\((.*?)\)", text)
    return matches

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    for index in range(0, len(blocks)):
        
        blocks[index] = blocks[index].strip("\n")
        if blocks[index] == "":
            blocks.remove(blocks[index])
    return blocks


def block_to_block_type(block):
    lines = block.split("\n")
    hash_char = "#"
    order_number = 1
    for line in lines:
        result = BlockType.PARAGRAPG
        for _ in range(0, 6):
            if re.findall(r"^" + hash_char + " ", line):
                result = BlockType.HEADING
            hash_char += "#"
        if re.findall(r"```[\s\S]*?```", line):
                result = BlockType.CODE
        if re.findall(r">", line):
                result = BlockType.QUOTE
        if re.findall(r"- ", line):
                result = BlockType.UNORDERED_LIST
        if re.findall(str(order_number) + ". ", line):
                result = BlockType.ORDERED_LIST
                order_number += 1
        
    return result
        


# md = """
# This is **bolded** paragraph

# This is another paragraph with _italic_ text and `code` here
# This is the same paragraph on a new line

# . This is a list
# - with items
# """
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

print(result)