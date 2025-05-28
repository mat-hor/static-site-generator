import markdown_utils, textnode_utils
import parentnode
from textnode import TextNode
import re
from os import listdir, path, mkdir
from shutil import rmtree, copy


def text_to_leafnode(text, delimeter, text_type):
    node = TextNode(text=text.replace(f"{delimeter}", "").lstrip(), text_type=text_type)
    child = textnode_utils.text_node_to_html_node(node)
    return child

def text_to_children(text):
    text_nodes = textnode_utils.text_to_textnodes(text)

    return list(map(lambda x: textnode_utils.text_node_to_html_node(x) ,text_nodes))
    
def markdown_to_html_node(markdown):
    # 8 additional helper function
    text_blocks = markdown_utils.markdown_to_blocks(markdown)

    elements = []
    for text_block in text_blocks:
        block_type = markdown_utils.block_to_block_type(text_block)

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
                hash_char = "#"
                for num in range(0, 6):
                    if re.findall(r"^" + hash_char + " ", text_block):
                        child = text_to_leafnode(text_block, f"{hash_char}", textnode_utils.TextType.TEXT)
                        child.tag = f"h{num + 1}"
                    hash_char += "#"
                block_parent = child
                
        
        elements.append(block_parent)

    html_parent = parentnode.ParentNode("div",elements)

    return html_parent

def create_file_folder_structure(src, dst):
    if path.exists(dst):
        rmtree(dst)
    mkdir(dst)
    copy_files(src,dst)
    
def copy_files(src, dest):
    elements = listdir(src)
    for element in elements:
        file_src = path.join(src, element)
        file_dest = path.join(dest, element)
        if path.isfile(file_src):
            copy(file_src, file_dest)
        else:
            mkdir(file_dest)
            copy_files(file_src, file_dest)

def extract_title(markdown):
    title = re.findall(r"^#.*", markdown)
    if len(title) == 0:
        raise Exception("No h1 header in markdown")
    return title[0].strip("#").strip()

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as file:
        markdown = file.read()

    with open(template_path) as file:
        template = file.read()

    node = markdown_to_html_node(markdown)
    page_content = node.to_html()
    page_title = extract_title(markdown)
    template = template.replace("{{ Title }}", page_title)
    template = template.replace("{{ Content }}", page_content)

    with open(dest_path, "w") as file:
        file.write(template)






def main():
    create_file_folder_structure("static", "public")
    
    generate_page("content/index.md", "template.html", "public/index.html")

main()
