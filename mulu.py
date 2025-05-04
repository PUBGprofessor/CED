from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage
# from pdfminer.pdfinterp import PDFInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from io import StringIO
import re
import argparse

def normalize(text):
    return text.strip().replace("、", "").replace(" ", "").replace("　", "")

def shared_prefix_ratio(title, text):
    """
    计算 title 和 text 前 min(len(title), len(text)) 个字符中的最长前缀相同长度，
    返回其占 title 长度的比例（考虑顺序）。
    """
    minlen = min(len(title), len(text))
    match_len = 0
    for i in range(minlen):
        if title[i] == text[i]:
            match_len += 1
        else:
            break
    minlen = max(10, minlen)
    # return match_len / len(title) if len(title) > 0 else 0
    return max(match_len / minlen, match_len / len(title)) if len(title) > 0 else 0


from difflib import SequenceMatcher

def fuzzy_match(text1, text2):
    """返回两个字符串的相似度"""
    return SequenceMatcher(None, text1, text2).ratio()


# def get_pdf_outlines(pdf_path):
#     outlines = []
#     with open(pdf_path, 'rb') as f:
#         parser = PDFParser(f)
#         doc = PDFDocument(parser)
#         if 'Outlines' not in doc.catalog:
#             print("PDF 没有目录书签")
#             return outlines
#         outlines_raw = doc.get_outlines()
#         for (level, title, dest, a, se) in outlines_raw:
#             outlines.append((level, title))
#     return outlines
import fitz  # pip install pymupdf

def get_pdf_outlines(pdf_path):
    doc = fitz.open(pdf_path)
    outlines = []
    for item in doc.get_toc():  # 返回列表，每项是 [level, title, page+1]
        level, title, page = item
        outlines.append((level, title, page))  # page 转换为从 1 开始
    return outlines


import csv

def match_outline_to_txt(txt_path, outlines, output_path, threshold=0.8):
    """
    txt_path: 输入TXT，每行如 [level, ..., page, text]
    outlines: [(level, title), ...]，按目录顺序排列
    output_path: 输出更新的TXT
    """
    rows = []
    with open(txt_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            rows.append(row)

    outline_idx = 0  # 当前处理到第几个目录
    # matched_titles = set()
    for row in rows:
        text = normalize(row[-1])
        page = int(row[-2])  # 倒数第二列是页码
        matched_level = 0

        while outline_idx < len(outlines):
            level, title, title_page = outlines[outline_idx]
            if page > title_page:
                outline_idx += 1
                continue
            title_norm = normalize(title)
            sim = shared_prefix_ratio(title_norm, text)
            if sim >= threshold:
                matched_level = level
                outline_idx += 1  # 顺序匹配，命中后不再尝试之前的目录
                break
            else:
                break  # 不回溯，不跳过目录项，顺序严格匹配

        row[0] = str(matched_level)  # 更新目录等级
        # row.append(f"匹配度:{sim:.2f}, 页码:{page}")  # 若要调试页码匹配情况

    # 写回文件
    with open(output_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(rows)

    print(f"已保存更新的TXT到 {output_path}")


def redeal(pdf_path, txt_path, output_path):
    outlines = get_pdf_outlines(pdf_path)
    match_outline_to_txt(txt_path, outlines, output_path)

if __name__ == '__main__':  
    parser = argparse.ArgumentParser(description="Match PDF outlines to TXT content.")
    parser.add_argument("-p", "--pdf_path", type=str, help="Path to the PDF file")
    parser.add_argument("-t", "--txt_path", type=str, help="Path to the extracted TXT file")
    parser.add_argument("-o", "--output_path", type=str, help="Path to save the matched outline result")

    args = parser.parse_args()

    outlines = get_pdf_outlines(args.pdf_path)
    match_outline_to_txt(args.txt_path, outlines, args.output_path)

