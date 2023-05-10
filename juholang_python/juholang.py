import sys
import re


class juholang:
    def __init__(self, path: str):
        self.VAR_CNT = 64
        self.variables = [0] * self.VAR_CNT

        # 파일을 열고 line마다 저장 후 닫기
        my_file = open(path, "rt", encoding='utf-8')
        delim = r'\n| '
        self.lines = re.split(delim, my_file.read().strip())
        my_file.close()

        if self.lines[0] != "주호야":
            print("Invalid BOF")
            return

        for line in self.lines:
            # print(line)
            self.interpret_line(line)

    @staticmethod
    def evaluate_increment_decrement_operator(cmd: str):
        value = 0
        for char in cmd:
            if char == '?':
                value += 1
            elif char == "!":
                value -= 1
            else:
                print(f"Invalid increment/decrement operator: {char}")
        return value

    def interpret_line(self, line: str):
        if "그래" in line:  # 변수의 대입
            line = line[2:]  # prefix 제거

            mul_char = 'ㅋ'
            div_char = 'ㅎ'
            mul_count = line.count(mul_char)
            div_count = line.count(div_char)
            if mul_count > 1 or div_count > 1 or (mul_count >= 1 and div_count >= 1):
                print("Invalid assignment operator")
                return

            var_idx = line.count('애')
            value = None
            if mul_count >= 1:
                lhs, rhs = line.split(sep=mul_char, maxsplit=1)
                lhs = self.evaluate_increment_decrement_operator(lhs[var_idx:])
                rhs = self.evaluate_increment_decrement_operator(rhs)
                value = lhs * rhs
            elif div_count >= 1:
                lhs, rhs = line.split(sep=div_char, maxsplit=1)
                lhs = self.evaluate_increment_decrement_operator(lhs[var_idx:])
                rhs = self.evaluate_increment_decrement_operator(rhs)
                value = lhs // rhs

            self.variables[var_idx] = value

        elif "맞아" in line:  # 변수의 증감
            line = line[2:]  # prefix 제거

            var_identifier = '~'
            var_idx = line.count(var_identifier)
            self.variables[var_idx] += self.evaluate_increment_decrement_operator(line[var_idx:])

        elif "인정" in line or "진짜" in line:  # 변수 출력

            CONSOLE_OUT_PARSE_VAR = 0x01
            CONSOLE_OUT_PARSE_EXP = 0x02
            CONSOLE_OUT_PRINT_INT = 0x04
            CONSOLE_OUT_PRINT_UNICODE = 0x08

            console_out_mode = 0

            if line[:2] == "인정":
                console_out_mode |= CONSOLE_OUT_PRINT_INT
            else:
                console_out_mode |= CONSOLE_OUT_PRINT_UNICODE

            line = line[2:]  # prefix 제거

            if line[0] == '.':
                console_out_mode |= CONSOLE_OUT_PARSE_VAR
            else:
                console_out_mode |= CONSOLE_OUT_PARSE_EXP

            var_identifier = '.'
            allowed_char_in_exp = ['!', '?', 'ㅋ', 'ㅎ']
            for char in line:
                if console_out_mode & CONSOLE_OUT_PARSE_VAR and char != var_identifier:
                    print("Invalid console output")
                    return

                if console_out_mode & CONSOLE_OUT_PARSE_EXP and char not in allowed_char_in_exp:
                    print("Invalid console output")
                    return

            value = None
            if console_out_mode & CONSOLE_OUT_PARSE_VAR:
                var_idx = line.count(var_identifier) - 1
                value = self.variables[var_idx]
            else:
                mul_char = 'ㅋ'
                div_char = 'ㅎ'
                mul_count = line.count(mul_char)
                div_count = line.count(div_char)
                if mul_count > 1 or div_count > 1 or (mul_count >= 1 and div_count >= 1):
                    print("Invalid increment/decrement operator")
                    return

                if mul_count >= 1:
                    lhs, rhs = line.split(sep=mul_char, maxsplit=1)
                    lhs = self.evaluate_increment_decrement_operator(lhs)
                    rhs = self.evaluate_increment_decrement_operator(rhs)
                    value = lhs * rhs
                elif div_count >= 1:
                    lhs, rhs = line.split(sep=div_char, maxsplit=1)
                    lhs = self.evaluate_increment_decrement_operator(lhs)
                    rhs = self.evaluate_increment_decrement_operator(rhs)
                    value = lhs // rhs

            if console_out_mode & CONSOLE_OUT_PRINT_UNICODE:
                value = chr(value)
            print(value, end='')

        elif "진짜" in line:  # 변수 출력(문자열)
            line = line[2:]  # prefix 제거


if __name__ == "__main__":
    interpreter = juholang("test.juho")
