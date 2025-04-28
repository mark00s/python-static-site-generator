from htmlnode import HTMLNode
from leafnode import LeafNode


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError("Tag value is missing in ParentNode")

        if not self.children:
            raise ValueError("Children value is missing in ParentNode")

        html = f"<{self.tag}>"
        if isinstance(self, LeafNode):
            return self.to_html()

        for child in self.children:
            html += child.to_html()

        html += f"</{self.tag}>"

        return html

    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"
