import sys
from lexer import MyLexer
from parser import MyParser
from analyzer import MyAnalyzer
from generator import generator


def read_input_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)


def write_output_file(file_path, code_lines):
    try:
        with open(file_path, 'w') as file:
            for line in code_lines:
                file.write(line + '\n')
    except Exception as e:
        print(f"Error writing to file: {e}")
        sys.exit(1)


def translate_code(input_text):
    lexer = MyLexer()
    parser = MyParser()

    tokens = lexer.tokenize(input_text)

    ast = parser.parse(tokens)

    analizer = MyAnalyzer()
    analizer.analyze(ast)
    data = analizer.get_data()
    code_generator = generator(data)
    code = code_generator.translate(ast)
    return code


def main():
    if len(sys.argv) != 3:
        print('Usage: python main.py <input_file_path> <output_file_path>')
        sys.exit(1)

    input_text = read_input_file(sys.argv[1])

    code = translate_code(input_text)

    write_output_file(sys.argv[2], code)


if __name__ == "__main__":
    main()
