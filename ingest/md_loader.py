"""
文件名：ingest/md_loader.py
最后修改时间：2026-04-16
模块功能：加载 Markdown 文档并转换为可切分的文本内容。
模块相关技术：LangChain Community、TextLoader、UTF-8 编码处理。
"""

from langchain_community.document_loaders import TextLoader


def load_markdown(file_path):
    loader = TextLoader(file_path, encoding="utf-8", autodetect_encoding=True)
    return loader.load()
