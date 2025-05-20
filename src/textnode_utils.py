from textnode import TextNode, TextType
from leafnode import LeafNode
from markdown_utils import extract_markdown_images, extract_markdown_links

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(tag = None, value=text_node.text)
        case TextType.BOLD:
            return LeafNode(tag = "b", value=text_node.text)
        case TextType.ITALIC:
            return LeafNode(tag = "i", value=text_node.text)
        case TextType.CODE:
            return LeafNode(tag = "code", value=text_node.text)
        case TextType.LINK:
            return LeafNode(tag = "a", value=text_node.text, props="href")
        case TextType.IMAGE:
            return LeafNode(tag = "img", value="", props={"src":text_node.url, "alt":text_node.text})
        case _:
            raise Exception("Undefined text type")

def split_nodes_delimiter(old_nodes, delimiter, text_type):

        new_nodes = []
        delimiter_found = False
        for old_node in old_nodes:
            if old_node.text_type != TextType.TEXT:
                new_nodes.append(TextNode(old_node.text, old_node.text_type))
                continue
            start_position = old_node.text.find(delimiter)
            if start_position == -1:
                new_nodes.append(TextNode(old_node.text, old_node.text_type))
                continue
            end_position = old_node.text[start_position+1:].find(delimiter)
            if end_position == -1:
                continue
            delimiter_found = True
            end_position += start_position
            inline_bloc_text = old_node.text[start_position+len(delimiter):end_position+1]
            splited_node_text = old_node.text.split(delimiter)
            
            for split_text in splited_node_text:
                
                if inline_bloc_text in split_text:
            
                    text_node = TextNode(split_text, text_type)
                    new_nodes.append(text_node)
                else:
                    text_node = TextNode(split_text, old_node.text_type)
                    new_nodes.append(text_node)

        if not delimiter_found:
            raise Exception("Delimiter not found")
        return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        links = extract_markdown_images(old_node.text)
        text = old_node.text
        for link in links:
            delimiter = f"![{link[0]}]({link[1]})"
            splited_text = text.split(delimiter, 1)
            new_nodes.append(TextNode(splited_text[0], TextType.TEXT))
            new_nodes.append(TextNode(link[0], TextType.IMAGE, link[1]))
            text = text.replace(splited_text[0], "")
            text = text.replace(delimiter, "")
  
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        links = extract_markdown_links(old_node.text)
        text = old_node.text
        for link in links:
            delimiter = f"[{link[0]}]({link[1]})"
            splited_text = text.split(delimiter, 1)
            new_nodes.append(TextNode(splited_text[0], TextType.TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            text = text.replace(splited_text[0], "")
            text = text.replace(delimiter, "")
  
    return new_nodes
    



