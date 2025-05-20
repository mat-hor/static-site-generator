from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag,  children=children, props=props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("tag is none")
        if self.children is None:
            raise ValueError("children is none")

        children_copy = self.children.copy()
        return f"<{self.tag}>{self.__get_children_html(children_copy)}</{self.tag}>"

    def __get_children_html(self, children):
        if len(children) == 0:
            return ""
        return children[0].to_html() + self.__get_children_html(children[1:])
        
