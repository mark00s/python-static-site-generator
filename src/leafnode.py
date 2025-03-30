from htmlnode import HTMLNode


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if not self.value:
            raise ValueError()
        if not self.tag:
            return f"{self.value}"
        
        props_html = ""
        if self.props:
            props_html = self.props_to_html()
        
        return f'<{self.tag}{props_html}>{self.value}</{self.tag}>'
