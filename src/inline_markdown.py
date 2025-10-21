import re

from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        sections = node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("Markdown formatting error. Section not closed")

        for i, section in enumerate(sections):
            # Last one can be empty ("")
            if section:
                if i % 2 == 0:
                    # Even, then around delimeters
                    new_nodes.append(TextNode(section, TextType.TEXT))
                else:
                    # Odd, then inside delimeters
                    new_nodes.append(TextNode(section, text_type))
    return new_nodes


def split_nodes_links_images(old_nodes, text_type: TextType, extract_method):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        original_text = node.text
        if len(original_text) == 0:
            continue
        mds = extract_method(original_text)
        if len(mds) == 0:
            new_nodes.append(node)
            continue
        for alt, link in mds:
            md_image = f"![{alt}]({link})"
            if text_type == TextType.LINK:
                md_image = md_image[1:]  # rm !
            if len(md_image) == len(original_text):
                new_nodes.append(TextNode(alt, text_type, link))
                original_text = ""
                continue
            sections = original_text.split(md_image, 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, image section not closed")
            new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(alt, text_type, link))
            # Trim original_text by sections[0] + md)image len
            original_text = original_text[(len(sections[0]) + len(md_image)) :]
        if len(original_text):
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    return nodes


def split_nodes_image(old_nodes: list[TextNode]):
    return split_nodes_links_images(old_nodes, TextType.IMAGE, extract_markdown_images)


def split_nodes_link(old_nodes):
    return split_nodes_links_images(old_nodes, TextType.LINK, extract_markdown_links)


def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)


def extract_markdown_links(text):
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)
