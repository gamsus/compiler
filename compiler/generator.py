def var_to_reg(var, reg):  # a i reg
    """
    Konwertuje zmienną na rejestr w assemblerze.
    :param var: Obiekt reprezentujący zmienną.
    :param reg: Nazwa docelowego rejestru.
    :return: Lista instrukcji assemblera potrzebnych do wykonania konwersji.
    """
    codes = []
    if var.is_in_register:
        # Jeśli zmienna już jest w rejestrze
        if reg == var.register:
            return codes
        else:
            # Jeśli docelowy rejestr jest inny niż aktualny rejestr zmiennej
            codes.append(f"GET {var.reg}")
            if reg != 'a':
                codes.append(f"PUT {reg}")
    else:
        # Jeśli zmienna jest w pamięci
        codes += num_to_reg(var.mem, reg)
        codes.append(f"LOAD {reg}")
        if reg != 'a':
            codes.append(f"PUT {reg}")  # Przenieś wartość do docelowego rejestru (jeśli różny niż 'a')

    return codes


def num_to_reg(num, reg):  # wczytuje num

    codes = [f"RST {reg} # tu", f"RST {reg}"]
    bin_r = bin(num)[2:]
    for i, a in enumerate(bin_r):
        if i != 0:
            codes.append(f"SHL {reg}")
        if a == '1':
            codes.append(f"INC {reg}")
    return codes


def save(reg, var, of):  # do pamieci z rejestrow [a, h]
    codes = []
    if reg != 'a':
        codes.append(f"PUT {reg}")
    codes += num_to_reg(var.mem + of, 'h')
    codes.append("STORE h #koniec")
    return codes


def save2(reg, var, of):  # do pamieci z rejestrow [a, h]
    codes = []
    if reg != 'a':
        codes.append(f"PUT {reg}")
    codes += num_to_reg(var.mem + of, 'h')
    codes.append("STORE h # tu")
    return codes


def expressions(operator, k=0):  # rejestry a, h
    codes = []
    if operator == '+':
        codes.append("ADD h")
    elif operator == '-':
        codes.append("SUB h")
    elif operator == '*':
        codes += ["PUT g", "SUB h", f"JPOS {k + 6}", "GET h", "PUT f", f"JPOS {k + 10}", "GET g", "PUT f", "GET h",
                  "PUT g", "RST h", "GET g", f"JZERO {k + 28}", "SHR a", "SHL a", "PUT e", "SUB g", "PUT d", "GET g",
                  "SUB e", "ADD d", f"JZERO {k + 25}", "GET h", "ADD f", "PUT h", "SHL f", "SHR g", f"JUMP {k + 11}",
                  "GET h"]
    elif operator == '/':
        codes += ["PUT f", "GET h", f"JZERO {k + 26}", "PUT g", "RST h", "GET g", "SUB f", f"JPOS {k + 26}", "RST e",
                  "INC e", "GET g",
                  "PUT d", "GET d", "SHL a", "SUB f", f"JPOS {k + 19}", "SHL d", "SHL e", f"JUMP {k + 12}", "GET f",
                  "SUB d", "PUT f", "GET h", "ADD e", "PUT h", f"JUMP {k + 5}", "GET h"]
    elif operator == '%':
        codes += ["PUT f", "GET h", f"JZERO {k + 23}", "PUT g", "GET g", "SUB f", f"JPOS {k + 22}", "RST e", "INC e",
                  "GET g", "PUT d",
                  "GET d", "SHL a", "SUB f", f"JPOS {k + 18}", "SHL d", "SHL e", f"JUMP {k + 11}", "GET f", "SUB d",
                  "PUT f", f"JUMP {k + 4}", "GET f"]

    return codes


class generator:
    def __init__(self, data):
        """
        Inicjalizuje obiekt klasy Generator.
        :param data: Lista danych wejściowych zawierająca deklaracje procedur, deklaracje główne i dostępne
        rejestry.
        """
        self.proc_dec = data[0]  # Deklaracje procedur.
        self.main_declarations = data[1]  # Deklaracje główne.
        self.free_registers = data[2]  # Dostępne rejestry.
        self.codes = []  # Lista instrukcji assemblera generowanych przez tłumaczenie.

    def translate(self, ast):
        """
        Tłumaczy abstrakcyjne drzewo składniowe (AST) na kod assemblera.
        :param ast: Abstrakcyjne drzewo składniowe reprezentujące program.
        :return: Lista instrukcji assemblera.
        """
        for procedure in ast[0]:
            proc_name = procedure[0][0]
            proc = self.proc_dec[proc_name]  # Pobierz deklarację procedury
            for node in procedure:
                if type(node) is int:
                    continue
                if node[0] == 'commands':
                    proc.set_commands(node[1])

        self.trans_main(ast[1])
        self.codes.append('HALT')  # Dodaj instrukcję HALT na koniec programu
        return self.codes

    def trans_main(self, main):
        for node in main:
            if node[0] == 'commands':
                for command in node[1]:
                    self.trans_c(command, 'main')

    def trans_c(self, com, place):
        if com[0] == 'ASSIGN':
            i = com[1]
            exp = com[2]
            if exp[0] == 'val':
                val = exp[1]
                if val[0] == 'number':
                    self.codes += num_to_reg(val[1], 'a')  # wynik
                if val[0] == 'iden':
                    self.load_iden(place, val[1], 'a')
                self.save_i(place, i, 'a')

            if exp[0] == 'ADD':
                val = exp[1]
                val2 = exp[2]
                self.load_from_val(place, val, 'b')  # potrzebny wolny rejestr
                self.load_from_val(place, val2, 'h')
                self.codes.append("GET b")
                self.codes += expressions('+')
                self.save_i(place, i, 'a')

            if exp[0] == 'SUB':
                val = exp[1]
                val2 = exp[2]
                self.load_from_val(place, val, 'b')
                self.load_from_val(place, val2, 'h')
                self.codes.append("GET b")
                self.codes += expressions('-')
                self.save_i(place, i, 'a')

            if exp[0] == 'MUL':
                val = exp[1]
                val2 = exp[2]
                if val2[0] == 'number' and val2[1] == 2:
                    self.load_from_val(place, val, 'a')
                    self.codes.append("SHL a")
                    self.save_i(place, i, 'a')
                else:
                    self.load_from_val(place, val, 'b')
                    self.load_from_val(place, val2, 'h')
                    self.codes.append("GET b")
                    self.codes += expressions('*', len(self.codes))
                    self.save_i(place, i, 'a')

            if exp[0] == 'DIV':
                val = exp[1]
                val2 = exp[2]
                if val2[0] == 'number' and val2[1] == 2:
                    self.load_from_val(place, val, 'a')
                    self.codes.append("SHR a")
                    self.save_i(place, i, 'a')
                else:
                    self.load_from_val(place, val, 'b')
                    self.load_from_val(place, val2, 'h')
                    self.codes.append("GET b")
                    self.codes += expressions('/', len(self.codes))
                    self.save_i(place, i, 'a')

            if exp[0] == 'MOD':
                val = exp[1]
                val2 = exp[2]
                self.load_from_val(place, val, 'b')
                self.load_from_val(place, val2, 'h')
                self.codes.append("GET b")
                self.codes += expressions('%', len(self.codes))
                self.save_i(place, i, 'a')
        if com[0] == 'IF':
            condition = com[1]
            commands = com[2][1]
            operator = condition[0]
            val = condition[1]
            val2 = condition[2]
            self.condition(operator, val, val2, place)
            k = len(self.codes)
            self.codes.append(" ")  # miejsce na JUMP
            for command in commands:
                self.trans_c(command, place)
            self.jump(com[1][0], k, len(self.codes))
        if com[0] == 'IFELSE':
            self.codes.append("RST c #pocztek ifelse")
            condition = com[1]
            commands = com[2][1]
            operator = condition[0]
            val = condition[1]
            val2 = condition[2]
            self.condition(operator, val, val2, place)
            k = len(self.codes)
            self.codes.append(" ")  # miejsce na JUMP
            for command in commands:
                self.trans_c(command, place)  # k to miejsce w kodzie gdzie bedzie JUMP IFA
            k2 = len(self.codes)
            self.codes.append(" ")  # miejsce na JUMP do konca IFELSE
            c_else = com[3][1]
            for command in c_else:
                self.trans_c(command, place)
            m = len(self.codes)
            self.jump(com[1][0], k, k2 + 1)
            self.codes[k2] = f"JUMP {m}"
            self.codes.append("RST c #koniec ifelse")
        if com[0] == 'WHILE':
            self.codes.append("RST c #poczotek while")
            commands = com[2][1]
            cond = com[1]
            op = cond[0]
            val = cond[1]
            val2 = cond[2]
            k = len(self.codes)
            self.condition(op, val, val2, place)
            k2 = len(self.codes)
            self.codes.append(" ")
            for command in commands:
                self.trans_c(command, place)
            self.codes.append(f"JUMP {k}")
            self.jump(op, k2, len(self.codes))
            self.codes.append("RST c #koniec while")
        if com[0] == 'REPEAT':
            commands = com[2][1]
            condition = com[1]
            operator = condition[0]
            k = len(self.codes)
            for command in commands:
                self.trans_c(command, place)
            val = condition[1]
            val2 = condition[2]
            self.condition(self.negation(operator), val, val2, place)
            k2 = len(self.codes)  # miejsce na JUMP
            self.codes.append(" ")
            self.codes.append(f"JUMP {k}")

            self.jump(self.negation(operator), k2, len(self.codes))
        if com[0] == 'READ':
            i = com[1]
            self.codes.append("READ")
            self.save_i(place, i, 'a')
        if com[0] == 'WRITE':
            val = com[1]
            self.load_from_val(place, val, 'a')
            self.codes.append("WRITE")
        if com[0] == 'proc_call':
            proc_name = com[1]
            proc = self.proc_dec[proc_name]
            args = []
            for var_name in com[2]:
                var = self.find_var(place, var_name)
                args.append(var)
            proc.set_arguments(args)
            self.codes.append("RST c # start")
            for command in proc.commands:
                self.trans_c(command, proc_name)
            self.codes.append("RST c # koniec")

    def jump(self, operator, k, k2):
        if operator == 'LE':
            self.codes[k] = f"JPOS {k2}"
        if operator == 'GE':
            self.codes[k] = f"JPOS {k2}"
        if operator == 'LT':
            self.codes[k] = f"JZERO {k2}"
        if operator == 'GT':
            self.codes[k] = f"JZERO {k2}"
        if operator == 'EQ':
            self.codes[k] = f"JPOS  {k2}"
        if operator == 'NEQ':
            self.codes[k] = f"JZERO {k2}"

    @staticmethod
    def negation(operetor):
        if operetor == 'LE':
            return 'GE'
        if operetor == 'GE':
            return 'LE'
        if operetor == 'LT':
            return 'GT'
        if operetor == 'GT':
            return 'LT'
        if operetor == 'EQ':
            return 'NEQ'
        if operetor == 'NEQ':
            return 'EQ'

    def condition(self, operation, val, val2, place):
        if operation == 'LE':
            self.load_from_val(place, val, 'b')
            self.load_from_val(place, val2, 'h')
            self.codes.append("GET b")
            self.codes.append("SUB h")
        if operation == 'GE':
            self.condition('LE', val2, val, place)

        if operation == 'GT':
            self.load_from_val(place, val, 'b')
            self.load_from_val(place, val2, 'h')
            self.codes.append("GET b")
            self.codes.append("SUB h")
        if operation == 'LT':
            self.condition('GT', val2, val, place)

        if operation in {'EQ', 'NEQ'}:
            self.load_from_val(place, val, 'b')
            self.load_from_val(place, val2, 'h')
            self.codes.append("GET b")
            self.codes.append("PUT g")
            self.codes.append("SUB h")
            self.codes.append("PUT f")
            self.codes.append("GET h")
            self.codes.append("SUB g")
            self.codes.append("ADD f")  # (a-h) + (h-a)

    def save_i(self, place, i, reg):  # do identificatora
        if i[0] == 'var':
            var = self.find_var(place, i[1])
            self.codes += save(reg, var, 0)

        elif i[0] == 'array_with_pid' or i[0] == 'array_with_num':
            var_name = i[1]
            var = self.find_var(place, var_name)

            if i[0] == 'array_with_pid':
                var2_name = i[2]
                var2 = self.find_var(place, var2_name)
                if reg != 'a' and reg != 'g':
                    self.codes.append(f"GET {reg}")
                if reg != 'g':
                    self.codes.append("PUT g")

                self.codes += var_to_reg(var2, 'h')
                self.codes += num_to_reg(var.mem, 'a')
                self.codes.append("ADD h")
                self.codes.append("PUT h")
                self.codes.append("GET g")
                self.codes.append("STORE h")

            if i[0] == 'array_with_num':
                num = i[2]
                self.codes += save2(reg, var, num)

    def load_from_val(self, place, val, reg):
        if val[0] == 'number':
            self.codes += num_to_reg(val[1], reg)
        if val[0] == 'iden':
            i = val[1]
            self.load_iden(place, i, reg)
        return

    def load_iden(self, place, i, reg):  # wczytuje wartosc z identyfikatora do rejestru
        if i[0] == 'var':
            var = self.find_var(place, i[1])
            self.codes += var_to_reg(var, reg)

        elif i[0] == 'array_with_pid' or i[0] == 'array_with_num':
            var_name = i[1]
            var = self.find_var(place, var_name)
            if i[0] == 'array_with_pid':  # wczytywanie array
                var2_name = i[2]
                var2 = self.find_var(place, var2_name)
                self.codes += var_to_reg(var2, 'h')  # uzywa rejestru a i h
                self.codes += num_to_reg(var.mem, 'a')
                self.codes.append("ADD h")
                self.codes.append("LOAD a")
                if reg != 'a':
                    self.codes.append(f"PUT {reg}")
            if i[0] == 'array_with_num':
                num = i[2]
                self.codes += num_to_reg(var.mem + num, reg)
                self.codes.append(f"LOAD {reg}")
                if reg != 'a':
                    self.codes.append(f"PUT {reg}")

    def find_var(self, place, var_name):  # znajduje nazwe zmienne i ja deklaruje
        var = None
        if place == 'main':
            var = self.main_declarations[var_name]
        else:
            if var_name in self.proc_dec[place].declarations:
                var = self.proc_dec[place].declarations[var_name]
            else:
                var = self.proc_dec[place].arg_map[var_name].var
        return var
