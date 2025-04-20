from pdfminer.layout import LTChar, LTPage, LTTextBox


def put(Box: LTTextBox, degree: int, fp) -> None:
    fp.write("p"+str(Box.pageid)+' ')
    for line in Box:
        for i in line:
            if isinstance(i, LTChar):
                fp.write(i.get_text())
    fp.write('**'+str(degree)+'\n')  # Box.fontname, Box.fontsize, Box.linewidth


Catalog_list = ['一、', '(一', '（一', '一)', '一）', '1、', '1.', '(1', '（1', '1)', '1）']
Catalog_list_len = len(Catalog_list)
numb_big = set('一二三四五六七八九十')
numb_small = set('1234567890')
left_bracket = set('(（')
right_bracket = set(')）')


def isCatalog_1(Box: LTTextBox) -> int:
    """判断该Box是几号标题（1~10），返回 1~10或 0"""
    global Catalog_list
    global Catalog_list_len
    line = Box._objs[0]
    if len(line._objs) > 1:
        str_ = line._objs[0].get_text() + line._objs[1].get_text()
        for i in range(1, Catalog_list_len+1):
            if str_ == Catalog_list[i-1]:
                return i
    return 0


def isSameDegree(t: int, Box0: LTTextBox, BoxN: LTTextBox, page_left_begin0: float, page_left_beginN: float) -> bool:
    """判断Box0和BoxN是否为同一级标题，t为标题的级别"""
    if (Box0.x0-page_left_begin0) - (BoxN.x0-page_left_beginN) > Box0.fontsize or \
            Box0.linewidth != BoxN.linewidth:
        return False
    global Catalog_list, numb_small, numb_big
    line = BoxN._objs[0]
    if len(line._objs) < 4:
        str_set = set(line.get_text())
    else:
        str_set = set(line._objs[0].get_text()+line._objs[1].get_text()+\
               line._objs[2].get_text()+line._objs[3].get_text())
    match t:
        case 1:
            if not str_set.isdisjoint(numb_big) and ('、' in str_set):
                return True
        case 2 | 3:
            if not str_set.isdisjoint(numb_big) and not str_set.isdisjoint(left_bracket):
                return True
        case 4 | 5:
            if not str_set.isdisjoint(numb_big) and not str_set.isdisjoint(right_bracket):
                return True
        case 6:
            if not str_set.isdisjoint(numb_small) and ('、' in str_set):
                return True
        case 7:
            if not str_set.isdisjoint(numb_small) and ('.' in str_set):
                return True
        case 7 | 8:
            if not str_set.isdisjoint(numb_small) and not str_set.isdisjoint(left_bracket):
                return True
        case 9 | 10:
            if not str_set.isdisjoint(numb_small) and not str_set.isdisjoint(right_bracket):
                return True
    return False


def ExtraCatalog(PageList: list[LTPage], fp) -> None:
    """
    提取一级目录
    :param PageList:
    :return:None
    """
    def subExtra(BL: list[LTTextBox], degree:int, fp) -> None:
        """
        提取二级及以下目录（递归）
        :return:None
        """
        nonlocal PageList
        for i in range(len(BL)-1):
            """对于每两个父级标题之间"""
            put(BL[i], degree, fp)
            degree_list = []
            count = 0
            for pageid in range(BL[i].pageid, BL[i+1].pageid+1):    # 在两个标题之间的页面上
                """遍历两个父级标题之间的Box"""
                for Box in PageList[pageid-1]:
                    if (Box.pageid != BL[i].pageid or Box.y0 < BL[i].y0) and \
                        (Box.pageid != BL[i+1].pageid or Box.y0 > BL[i+1].y0):
                        if count == 0:
                            t = isCatalog_1(Box)
                            if t:
                                degree_list.append(Box)
                                count += 1
                        elif isSameDegree(t, degree_list[0], Box, PageList[degree_list[0].pageid-1].left_begin,
                                          PageList[pageid-1].left_begin):
                            if degree_list[count-1].pageid == Box.pageid and degree_list[count-1].y0 - Box.y1 < Box.fontsize:
                                """两标题距离过近，则不认为是标题"""
                                degree_list.clear()
                                count = 0
                            else:
                                degree_list.append(Box)
                                count += 1
                        else:
                            pass
            if len(degree_list) > 0:  # 有可提取的目录
                degree_list.append(BL[i+1])
                subExtra(degree_list, degree+1, fp)

    pageNumb = len(PageList)
    # pre = LTTextBox() #第一遍递归时，前一个元素LTTextBox设为空的
    frist_list = []
    for pageid in range(1, pageNumb+1):
        for Box in PageList[pageid-1]:
            if Box.isCenter(PageList[pageid-1].x0, PageList[pageid-1].x1, PageList[pageid-1].left_begin) and Box.linewidth > 0 and Box.fontsize > 10.56:
                frist_list.append(Box)
            last_Box = Box
    frist_list.append(last_Box)
    subExtra(frist_list, 1, fp)


