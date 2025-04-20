from deal import deal_pdf

if __name__ == '__main__':
    pdfName = r"E:\pythonProject\工大目录抽取数据集\281834793.pdf"
    # pdfName = r"..\兴业股份：兴业股份2023年年度报告.pdf"
    txtName = r'output\281834793.txt'
    with open(txtName, 'w', encoding='utf-8') as fp:
        deal_pdf(pdfName, fp)
