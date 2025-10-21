def markdown_to_blocks(markdown: str):
    result = []
    blocks = markdown.split("\n\n")
    for block in blocks:
        stripped = block.strip()
        if len(stripped):
            result.append(stripped)
    return result
