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
            return LeafNode(tag = "a", value=text_node.text, props={"href":text_node.url})
        case TextType.IMAGE:
            return LeafNode(tag = "img", value="", props={"src":text_node.url, "alt":text_node.text})
        case _:
            raise Exception("Undefined text type")

def split_nodes_delimiter(old_nodes, delimiter, text_type):

        new_nodes = []
        for old_node in old_nodes:
            if old_node.text_type != TextType.TEXT:
                new_nodes.append(TextNode(old_node.text, old_node.text_type))
                continue
            
            text = old_node.text
            splited_text  = text.split(delimiter)
            if len(splited_text) % 2 == 0:
                raise Exception("No closing delimiter")
            for idx in range(0, len(splited_text)):
                if idx % 2 == 0:
                    new_nodes.append(TextNode(splited_text[idx], TextType.TEXT))
                else:
                    new_nodes.append(TextNode(splited_text[idx], text_type))
                            
        return new_nodes


def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        images = extract_markdown_images(old_node.text)
        if len(images) == 0:
            new_nodes.append(old_node)
            continue
        text = old_node.text
        for image in images:
            delimiter = f"![{image[0]}]({image[1]})"
            splited_text = text.split(delimiter, 1)
            new_nodes.append(TextNode(splited_text[0], TextType.TEXT))
            new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
            text = text.replace(splited_text[0], "")
            text = text.replace(delimiter, "")
        if text.strip() != "":
            new_nodes.append(TextNode(text, TextType.TEXT))
  
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        links = extract_markdown_links(old_node.text)
        if len(links) == 0:
            new_nodes.append(old_node)
            continue
        text = old_node.text
        for link in links:
            delimiter = f"[{link[0]}]({link[1]})"
            splited_text = text.split(delimiter, 1)
            if splited_text[0].strip() != "":
                new_nodes.append(TextNode(splited_text[0], TextType.TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            text = text.replace(splited_text[0], "")
            text = text.replace(delimiter, "")
        if text.strip() != "":
            new_nodes.append(TextNode(text, TextType.TEXT))
  
    return new_nodes

def clean_text(text):
    return " ".join(list(map(lambda x: x.strip(), text.split("\n"))))
    
def text_to_textnodes(text):
    text = clean_text(text)
    node = TextNode(text, TextType.TEXT)
    new_node = split_nodes_delimiter([node], "**", TextType.BOLD)
    new_node = split_nodes_delimiter(new_node, "_", TextType.ITALIC)
    new_node = split_nodes_delimiter(new_node, "`", TextType.CODE)
    new_node = split_nodes_image(new_node)
    new_node = split_nodes_link(new_node)
    
    return new_node




