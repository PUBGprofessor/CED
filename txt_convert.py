import argparse

def convert_txt_to_outline_format(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as fin:
        lines = [line.strip() for line in fin if line.strip()]
    
    output_lines = []
    for line in lines:
        fields = line.split(',')
        if len(fields) < 10:
            continue

        label = int(fields[0])
        if label == 0:
            continue

        text = fields[9].strip()
        output_lines.append(f"{text} **{label}")
    
    with open(output_file, 'w', encoding='utf-8') as fout:
        fout.write('\n'.join(output_lines) + '\n')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert labeled TXT to outline format.")
    parser.add_argument("-i","--input_file", type=str, help="Path to input TXT file")
    parser.add_argument("-o","--output_file", type=str, help="Path to save converted output")

    args = parser.parse_args()
    convert_txt_to_outline_format(args.input_file, args.output_file)
