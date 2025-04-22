import argparse
from deal import deal_pdf

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extract text from a PDF file.')
    parser.add_argument('-d', '--pdf_path', required=True, help='Path to the input PDF file')
    parser.add_argument('-o', '--output_path', required=True, help='Path to the output TXT file')

    args = parser.parse_args()

    with open(args.output_path, 'w', encoding='utf-8') as fp:
        deal_pdf(args.pdf_path, fp)
    print(f"Done")
