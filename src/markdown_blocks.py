from enum import Enum
import re

from htmlnode import HTMLNode
from inline_markdown import text_to_textnodes
from leafnode import LeafNode
from parentnode import ParentNode
from textnode import TextNode, TextType, text_node_to_html_node


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if len(block) == 0:
            continue
        stripped = block.strip()
        filtered_blocks.append(stripped)
    return filtered_blocks


def block_to_block_type(block: str):
    # Headings start with 1-6 # characters, followed by a space and then the heading text.
    headings = re.findall(r"(^#{1,6} )(.)", block)
    if len(headings):
        if len(headings[0]) > 1:
            return BlockType.HEADING

    # Code blocks must start with 3 backticks and end with 3 backticks.
    code = re.findall(r"```[\s\S]*?```", block)
    if len(code):
        return BlockType.CODE

    # Every line in a quote block must start with a ">" character.
    if check_if_lines_starts_with(block, ">"):
        return BlockType.QUOTE

    # Every line in an unordered list block must start with a - character, followed by a space.
    if check_if_lines_starts_with(block, "- "):
        return BlockType.UNORDERED_LIST

    # Every line in an ordered list block must start with a number followed by a . character and a space.
    # The number must start at 1 and increment by 1 for each line.
    if check_if_ordered_list(block):
        return BlockType.ORDERED_LIST

    # If none of the above conditions are met, the block is a normal paragraph.
    return BlockType.PARAGRAPH


def check_if_lines_starts_with(lines: str, starter: str):
    split_lines = lines.split("\n")
    for line in split_lines:
        if not line.startswith(starter):
            return False
    return True


# Every line in an ordered list block must start with a number followed by a . character and a space.
# The number must start at 1 and increment by 1 for each line.
def check_if_ordered_list(lines: str):
    split_lines = lines.split("\n")
    for i, line in enumerate(split_lines):
        if len(line) <= 3:
            return False
        if not line[0].isnumeric():
            return False
        if not int(line[0]) == (i + 1):
            return False
        if not line[1] == ".":
            return False
        if not line[2] == " ":
            return False
    return True


def markdown_to_html_node(markdown: str) -> HTMLNode:
    blocks = markdown_to_blocks(markdown)
    nodes = []
    for block in blocks:
        if len(block) == 0:
            continue
        block_type = block_to_block_type(block)
        node = None
        match block_type:
            case BlockType.PARAGRAPH:
                node = ParentNode("p", text_to_children(block))
            case BlockType.HEADING:
                hashes = block.split()[0]
                text = block.removeprefix(f"{hashes} ")
                node = ParentNode("h" + str(len(hashes)), text_to_children(text))
            case BlockType.CODE:
                text = block.removeprefix("```\n").removesuffix("```")
                leaf = text_node_to_html_node(TextNode(text, TextType.CODE))
                node = ParentNode("pre", [leaf])
            case BlockType.QUOTE:
                leaf = quote_to_leaf_nodes(block)
                node = ParentNode("blockquote", leaf)
            case BlockType.UNORDERED_LIST:
                node = ParentNode("ul", split_list(block, "li", 2))
            case BlockType.ORDERED_LIST:
                node = ParentNode("ol", split_list(block, "li", 3))
        nodes.append(node)

    return ParentNode("div", nodes)


def text_to_children(block: str) -> list[LeafNode]:
    children = []
    text = block.replace("\n", " ")
    text_nodes = text_to_textnodes(text)
    for text_node in text_nodes:
        children.append(text_node_to_html_node(text_node))
    return children


def split_list(block: str, tag: str, size: int):
    children = []
    lines = block.split("\n")
    for line in lines:
        text = line[size:]
        leafs = text_to_children(text)
        children.append(ParentNode(tag, leafs))
    return children


def quote_to_leaf_nodes(block: str):
    lines = block.split("\n")
    trimmed_lines = []
    for line in lines:
        trimmed_lines.append(line.lstrip(">").strip())
    text = " ".join(trimmed_lines)
    return text_to_children(text)
