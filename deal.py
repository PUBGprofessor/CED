from interval import Interval
from pdfminer.high_level import extract_pages
from pdfminer.layout import *

from utils import IntervalSet, isNone, isSameStyle
from Extract import ExtraCatalog, put
import time

def deal_pdf(pdfname:str, fp, x)->None:
    """预处理1"""
    PageList = []   # pages: page列表
    count = 0
    # f1 = open(r'output\48870010_.txt', 'w')
    #       page             pages
    time1 = time.time()
    for page_layout in extract_pages(pdfname):
        """分别对每个Page进行处理"""
        count += 1
        objlist = LTPage(count, page_layout.bbox)   # 临时的page容器
        objlist_new = LTPage(count, page_layout.bbox)   # 最终保存的page容器
        area = IntervalSet()    # y轴矩阵范围
        # if page_layout.y1 > page_layout.x1: # 竖页
        #     area.append(Interval(0, page_layout.height * 0.08))  # 去除页脚：页面下端的8%
        #     area.append(Interval(page_layout.height * 0.92, page_layout.height)) # 去除页眉：页面上端的8%
        # else: # 横页
        #     area.append(Interval(0, page_layout.height * 0.12))  # 去除页脚：页面下端的12%
        #     area.append(Interval(page_layout.height * 0.88, page_layout.height))  # 去除页眉：页面上端的12%
        left_begin = objlist.left_begin   # 初始左边界（页面左端20%处）
        right_begin = objlist.right_begin   # 初始右边界（页面右端20%处）先用着，后面要改（初始化为页面边缘）
        # element(Box or Line)      page

        # 清理页面内容，去除表格
        for element in page_layout:
            # f1.write(element.__repr__()+'\n')
            if isinstance(element, LTRect):  # 如果是矩阵，将其y范围加入area
                if element.y1 - element.y0 > 1:
                    area.append(Interval(element.y0, element.y1))
            elif isinstance(element, LTTextBoxHorizontal):  # 如果是Box，将其分解为Line
                for i in element:
                    isNone(i) or objlist.add(i)
                    # isNone()去除不包含文字的LTTextline
            elif isinstance(element, LTTextLineHorizontal):  # 如果是Line，判断空白后加入
                isNone(element) or objlist.add(element)
            # else: #测试片段
            #     print(element, "?")

        for i in objlist:     # i均为LTTextLineHorizontal对象
            if i.y0 not in area:    # 左下角不在表格区域内（则整体不在表格区域内），则加入容器
                objlist_new.add(i)
                # 下面为更新左右边界
                if i.x0 < left_begin:
                    left_begin = i.x0
                if i.x1 > right_begin:
                    right_begin = i.x1

        objlist_new.left_begin = left_begin
        objlist_new.right_begin = right_begin

        PageList.append(objlist_new)
    time2 = time.time()
    # print("预处理1耗时：", time2 - time1, "秒") # 最多，20+s

    """预处理2：为LTTextlineH增加属性（信息）"""
    for page in PageList:
        for line in page:
            line.getInform(page.pageid)    # 给line赋值Char的部分属性：fontname, fontsize, linewidth, pageid
    time3 = time.time()
    # print("预处理2耗时：", time3 - time2, "秒")

    """预处理3：段落合并，全部转为LTTextBoxH"""
    for pageid in range(1, len(PageList)+1):
        """从第一页开始，对于每一页"""
        page_old = PageList[pageid-1]
        page_new = LTPage(pageid, page_old.bbox)  # 空的新页面
        page_new.left_begin = page_old.left_begin
        page_new.right_begin = page_old.left_begin
        i = 0
        while i < len(page_old._objs):
            """将页面里的内容全部换为合并后的LTTextBox"""
            LTB = LTTextBox()
            LTB.add(page_old._objs[i])
            while i+1 < len(page_old._objs) and isSameStyle(page_old._objs[i], page_old._objs[i+1], page_old):
                LTB.add(page_old._objs[i+1])
                # print(type(page_old._objs[i+1]))
                i += 1
            LTB.getInform(pageid)
            LTB.left = LTB.x0 / page_old.width
            LTB.center = (LTB.x1 + LTB.x0) / 2 / page_old.width
            LTB.top = LTB.y1
            LTB.bottom = LTB.y0
            page_new.add(LTB)
            i += 1
        PageList[pageid-1] = page_new
    time4 = time.time()
    # print("预处理3耗时：", time4 - time3, "秒")

    if not x:
        """直接写入txt特征，不进行目录提取"""
        for page in PageList:
            for LTB in page:
                put(LTB, 0, fp)  # 0表示没有标题
    else:
        """目录提取递归后写入txt"""
        ExtraCatalog(PageList, fp)
