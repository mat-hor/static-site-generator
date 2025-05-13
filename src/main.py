from textnode import TextNode, TextType

def main():
    x = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(x)

main()
