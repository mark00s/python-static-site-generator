from enum import Enum
import re


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown: str):
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
