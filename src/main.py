import markdown_utils, textnode_utils
import parentnode
from textnode import TextNode
import re
from os import listdir, path, mkdir
from shutil import rmtree, copy
from sys import argv


def text_to_leafnode(text, delimeter):
    text = text.replace(f"{delimeter}", "").lstrip()
    text_nodes = textnode_utils.text_to_textnodes(text)
    
    return list(map(lambda x: textnode_utils.text_node_to_html_node(x) ,text_nodes))

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
                child = text_to_leafnode(text_block, ">")
                child[0].tag = "blockquote"
                block_parent = child[0]

            case markdown_utils.BlockType.UNORDERED_LIST:
                list_items = text_block.split("\n")
                unordered_list_children = []
                for list_item in list_items:
                    child = text_to_leafnode(list_item, "-")
                    unordered_list_children.append(parentnode.ParentNode("li",child))
                block_parent = parentnode.ParentNode("ul",unordered_list_children)
                                         

            case markdown_utils.BlockType.ORDERED_LIST:
                list_items = text_block.split("\n")
                unordered_list_children = []
                order_number = 1
                for list_item in list_items:
                    child = text_to_leafnode(list_item, f"{order_number}.")
                    unordered_list_children.append(parentnode.ParentNode("li",child))
                    order_number += 1
                block_parent = parentnode.ParentNode("ol",unordered_list_children)

            case markdown_utils.BlockType.HEADING:
                hash_char = "#"
                for num in range(0, 6):
                    if re.findall(r"^" + hash_char + " ", text_block):
                        child = text_to_leafnode(text_block, f"{hash_char}")
                        child[0].tag = f"h{num + 1}"
                    hash_char += "#"
                block_parent = child[0]
                
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

def generate_page(from_path, template_path, dest_path, basepath):
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
    template = template.replace('href="/', f'href="{basepath}')
    template = template.replace('src="/', f'src="{basepath}')
    with open(dest_path, "w") as file:
        file.write(template)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    elements = listdir(dir_path_content)

    for element in elements:
        file_src = path.join(dir_path_content, element)
        file_dest = path.join(dest_dir_path, element)
        if path.isfile(file_src):
            if file_src.find("index.md") > 0:
                generate_page(file_src, template_path, f"{dest_dir_path}/index.html", basepath)
        else:
            mkdir(file_dest)
            generate_pages_recursive(file_src, template_path, file_dest, basepath)

def main():

    if len(argv) > 1:
        basepath = argv[1]
    else:
        basepath = "/"

    build_site_into = "docs"
    create_file_folder_structure("static", build_site_into)
    
    generate_pages_recursive("content", "template.html", build_site_into, basepath)

main()
