from textnode import TextNode, TextType
from leafnode import LeafNode

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