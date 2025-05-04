import argparse
from deal import deal_pdf

def deal(pdf_path, output_path):
    with open(output_path, 'w', encoding='utf-8') as fp:
        deal_pdf(pdf_path, fp, True)
    print(f"{pdf_path}: Done")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extract text from a PDF file.')
    parser.add_argument('-d', '--pdf_path', required=True, help='Path to the input PDF file')
    parser.add_argument('-o', '--output_path', required=True, help='Path to the output TXT file')
    parser.add_argument('--x', dest='x', action='store_false', help='是否进行基于规则的目录提取, 默认进行')

    args = parser.parse_args()

    with open(args.output_path, 'w', encoding='utf-8') as fp:
        deal_pdf(args.pdf_path, fp, args.x)
    print(f"{args.pdf_path}: Done")
