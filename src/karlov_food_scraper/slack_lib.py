def mrkdwn_section(text: str) -> dict:
    return {"type": "section", "text": {"type": "mrkdwn", "text": text}}


def header(text: str) -> dict:
    return {"type": "header", "text": {"type": "plain_text", "text": text, "emoji": True}}


def plain_context(text: str) -> dict:
    return {"type": "context", "elements": [{"type": "plain_text", "text": text, "emoji": True}]}


# def field(text: str) -> dict:
#     return {"type": "plain_text", "text": text, "emoji": True}


# def _fields_section(fields: list[str]) -> dict:
#     return {
#         "type": "section",
#         "fields": [field(f) for f in fields],
#     }


# def fields_sections(fields: list[str]) -> list[dict]:
#     if len(fields) > 10:
#         return [_fields_section(fields[:10])] + fields_sections(fields[10:])
#     else:
#         return [_fields_section(fields)]


def divider() -> dict:
    return {"type": "divider"}
