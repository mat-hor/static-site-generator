import markdown_utils, textnode_utils
import parentnode
from textnode import TextNode


def text_to_children(text):
    text_nodes = textnode_utils.text_to_textnodes(text)
    return list(map(lambda x: textnode_utils.text_node_to_html_node(x) ,text_nodes))
    
def markdown_to_html_node(markdown):
    # 8 additional helper function
    text_blocks = markdown_utils.markdown_to_blocks(markdown)

    elements = []
    for text_block in text_blocks:
        block_type = markdown_utils.block_to_block_type(text_block)
        print("BLOCK TYPE:", block_type)
        if block_type == markdown_utils.BlockType.CODE:
            
            code_node = TextNode(text=text_block.replace("```", "").lstrip(), text_type=textnode_utils.TextType.CODE)
            children = [textnode_utils.text_node_to_html_node(code_node)]
            block_parent = parentnode.ParentNode("pre",children)
        else:
            children = text_to_children(text_block)

            block_parent = parentnode.ParentNode("blockquote",children)
        # print(block_parent)
        elements.append(block_parent)

    
    html_parent = parentnode.ParentNode("div",elements)

    return html_parent


def main():

    md = """
> This is a quote.
"""



    node = markdown_to_html_node(md)
    print(node.to_html())


    "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>"


main()


'<div[41 chars]main\nthe **same** even with inline stuff</code></pre></div>'
'<div[41 chars]main\nthe **same** even with inline stuff\n</code></pre></div>'
