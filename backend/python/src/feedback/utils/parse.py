# ruff: noqa: PLC0206
import io
import zipfile

from docx import Document
from fastapi import UploadFile
from lxml import etree  # type: ignore

__all__ = ["read_docx", "extract_docx_comments"]


W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
NS = {"w": W}


async def extract_docx_comments(file: UploadFile) -> list[tuple[str, str]]:
    docx_bytes = await file.read()

    with zipfile.ZipFile(io.BytesIO(docx_bytes)) as z:
        doc_xml = etree.fromstring(z.read("word/document.xml"))

        if "word/comments.xml" not in z.namelist():
            return []

        comments_xml = etree.fromstring(z.read("word/comments.xml"))

    comment_map: dict[str, str] = {}
    for comment in comments_xml.findall(".//w:comment", NS):
        comment_id = comment.get(f"{{{W}}}id")
        text = "".join(t.text or "" for t in comment.findall(".//w:t", NS))
        comment_map[comment_id] = text

    body = doc_xml.find(f"{{{W}}}body")
    pairs: list[tuple[str, str]] = []

    for para in body.iter(f"{{{W}}}p"):
        children = list(para.iter())

        open_ranges: dict[str, list[str]] = {}

        for el in children:
            tag = el.tag

            if tag == f"{{{W}}}commentRangeStart":
                cid = el.get(f"{{{W}}}id")
                open_ranges[cid] = []

            elif tag == f"{{{W}}}t":
                for cid in open_ranges:
                    open_ranges[cid].append(el.text or "")

            elif tag == f"{{{W}}}commentRangeEnd":
                cid = el.get(f"{{{W}}}id")
                if cid in open_ranges:
                    highlighted_text = "".join(open_ranges.pop(cid))
                    comment_text = comment_map.get(cid, "")
                    if highlighted_text and comment_text:
                        pairs.append((highlighted_text, comment_text))

    return pairs


async def read_docx(file: UploadFile) -> str:
    contents = await file.read()
    doc = Document(io.BytesIO(contents))
    return "\n".join([para.text for para in doc.paragraphs if para.text.strip()])
