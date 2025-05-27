import markdown_utils, textnode_utils
import parentnode
from textnode import TextNode


def text_to_leafnode(text, delimeter, text_type):
    node = TextNode(text=text.replace(f"{delimeter}", "").lstrip(), text_type=text_type)
    child = textnode_utils.text_node_to_html_node(node)
    return child

def text_to_children(text):
    text_nodes = textnode_utils.text_to_textnodes(text)
    print(text_nodes)
    return list(map(lambda x: textnode_utils.text_node_to_html_node(x) ,text_nodes))
    
def markdown_to_html_node(markdown):
    # 8 additional helper function
    text_blocks = markdown_utils.markdown_to_blocks(markdown)

    elements = []
    for text_block in text_blocks:
        block_type = markdown_utils.block_to_block_type(text_block)
        print("BLOCK TYPE:", block_type)
        match block_type:
            case markdown_utils.BlockType.CODE:    
                code_node = TextNode(text=text_block.replace("```", "").lstrip(), text_type=textnode_utils.TextType.CODE)
                children = [textnode_utils.text_node_to_html_node(code_node)]
                block_parent = parentnode.ParentNode("pre",children)

            case markdown_utils.BlockType.PARAGRAPG:
                children = text_to_children(text_block)
                block_parent = parentnode.ParentNode("p",children)

            case markdown_utils.BlockType.QUOTE:
                child = text_to_leafnode(text_block, ">", textnode_utils.TextType.TEXT)
                child.tag = "blockquote"
                block_parent = child

            case markdown_utils.BlockType.UNORDERED_LIST:
                list_items = text_block.split("\n")
                unordered_list_children = []
                for list_item in list_items:
                    child = text_to_leafnode(list_item, "-", textnode_utils.TextType.TEXT)
                    child.tag = "li"
                    unordered_list_children.append(child)
                block_parent = parentnode.ParentNode("ul",unordered_list_children)
                                         

            case markdown_utils.BlockType.ORDERED_LIST:
                list_items = text_block.split("\n")
                unordered_list_children = []
                for list_item in list_items:
                    child = text_to_leafnode(list_item, "-", textnode_utils.TextType.TEXT)
                    child.tag = "li"
                    unordered_list_children.append(child)
                block_parent = parentnode.ParentNode("ol",unordered_list_children)

            case markdown_utils.BlockType.HEADING:
                child = text_to_leafnode(text_block, "#", textnode_utils.TextType.TEXT)
                child.tag = "h1"
                block_parent = child
                
        
        elements.append(block_parent)

    html_parent = parentnode.ParentNode("div",elements)

    return html_parent


def main():
    pass

main()
