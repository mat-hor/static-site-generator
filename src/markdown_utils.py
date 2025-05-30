import re
from enum import Enum
from htmlnode import HTMLNode



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
        if blocks[index].strip() == "":
            blocks.remove(blocks[index])
    return blocks


def block_to_block_type(block):
    line = block
    hash_char = "#"
    result = BlockType.PARAGRAPG
    for _ in range(0, 6):
        if re.findall(r"^" + hash_char + " ", line):
            result = BlockType.HEADING
        hash_char += "#"
    if re.findall(r"```[\s\S]*?```", line):
            result = BlockType.CODE
    if re.findall(r"^> ", line):
            result = BlockType.QUOTE
    if re.findall(r"^- ", line):
            result = BlockType.UNORDERED_LIST
    if re.findall("1. ", line):
            result = BlockType.ORDERED_LIST
        
    return result
        

