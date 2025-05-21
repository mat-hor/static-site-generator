import re

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


markdown = """
# This is a heading

This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

- This is the first list item in a list block
- This is a list item
- This is another list item
"""

print(markdown_to_blocks(markdown))