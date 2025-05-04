from interval import Interval
from pdfminer.layout import LTTextLineHorizontal, LTPage


class IntervalSet(list[Interval]):
    """
        元素为区间的一种列表
    """
    def __init__(self, *item):
        super().__init__(*item)

    def __contains__(self, obj: float) -> bool:
        for i in self:
            if obj in i:
                return True
        return False


def isNone(LTT:LTTextLineHorizontal) -> bool:
    """
    如果文本全部由EmptyCharList列表中的元素构成，则认为是None
    :param LTT:
    :return:bool
    """
    EmptyCharList = [' ', '\n']
    for i in LTT.get_text():
        if i not in EmptyCharList:
            return False
    return True

def isSameStyle(LTL1:LTTextLineHorizontal, LTL2:LTTextLineHorizontal, page:LTPage) -> bool:
    # 判断两行是否为同一段落
    if LTL1.isCenter(page.x0, page.x1, page.left_begin):
        return LTL2.isCenter(page.x0, page.x1, page.left_begin) and \
            LTL1.fontname == LTL2.fontname and \
            LTL1.fontsize == LTL2.fontsize and \
            LTL1.linewidth == LTL2.linewidth
    else:
        return LTL1.isEnd(page.right_begin) and \
            LTL1.fontname == LTL2.fontname and \
            LTL1.fontsize == LTL2.fontsize and \
            LTL1.linewidth == LTL2.linewidth and \
            LTL2.isFullOut(page.left_begin) # 顶格
