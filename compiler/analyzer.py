import sys


class Arg:
    def __init__(self, name, type, proc_name):
        """
                Inicjalizuje obiekt klasy Arg.

                :param name: Nazwa argumentu.
                :param type: Typ argumentu.
                :param proc_name: Nazwa procedury, do której argument należy.
                """
        self.var = None  # Zmienna, do której przypisany jest argument.
        self.name = name  # nazwa argumentu
        self.type = type  # typ argumentu
        self.proc_name = proc_name  # Nazwa procedury, do której argument należy.
        self.mem = None  # Pamięć, do której jest przypisany argument.
        self.is_assigning = False  # Flaga wskazująca, czy następuje przypisanie wartości argumentu.

    def set_var(self, var):
        """
                Ustawia zmienną, do której przypisany jest argument.
                :param var: Zmienna, do której ma być przypisany argument.
                """
        self.var = var


def error(error_message):
    print("ERR", error_message)
    sys.exit(1)


class Variable:
    def __init__(self, name, type, place, size=1):
        self.name = name  # var name
        self.type = type  # var type
        self.place = place  # gdzie sie znajduje
        self.size = size  # rozmiar gdy tablica
        self.is_Assigned = False
        self.is_in_register = False
        self.reg = None
        self.mem = None

    def set_mem(self, mem):
        self.mem = mem


class Procedure:
    def __init__(self, name):
        self.commands = []  # lista komend
        self.name = name  # nazwa procedury
        self.number = 0  # numer wywolania
        self.declarations = dict()  # mapa zmiennych
        self.arg_map = dict()  # mapa argumentow
        self.arg_list = []  # lista argumentow

    def set_arguments(self, var_list):
        for i, var in enumerate(var_list):
            self.arg_list[i].set_var(var)

    def inc_call_num(self):
        self.number += 1

    def set_commands(self, commands):
        self.commands = commands


class MyAnalyzer:

    def __init__(self):
        """
                Inicjalizuje obiekt klasy MyAnalyzer.

                Inicjalizuje różne właściwości, takie jak licznik 'k', mapy deklaracji, rejestry stałe i wolne.

        """
        self.k = 0  # Licznik używany do numerowania elementów w analizie.
        self.main_declarations = dict()  # mapa deklaracji
        self.proc_declarations = dict()  # mapa procedur
        self.fixed_registers = {"a", "h"}  # rejestry ktore sa zawsze zajete
        self.free_registers = {"b", "c", "d", "e", "f", "g"}  # rejestry ktore sa wolne

    def analyze(self, AST):  # analizuje skladnie i zbiera data
        for procedure in AST[0]:
            proc_head = procedure[0]
            proc_name = proc_head[0]
            k = procedure[-1]
            arguments = proc_head[1]

            proc = Procedure(proc_name)
            proc.proc_head = self.head(proc_head)
            if proc_name in self.proc_declarations.keys():
                error(f"Line: {k} Procedure name '{proc_name}' redefinition")
            else:
                self.proc_declarations[proc_name] = proc

            for argument in arguments:  # dodanie argumentow
                t = argument[0]
                arr_name = argument[1]
                if t == 'var':
                    arr = Arg(arr_name, 'var', proc_name)
                    proc.arg_map[arr_name] = arr
                    proc.arg_list.append(arr)
                else:
                    arr = Arg(arr_name, 'array_with_pid', proc_name)
                    proc.arg_map[arr_name] = arr
                    proc.arg_list.append(arr)

            for node in procedure:
                if type(node) is int:
                    continue

                if node[0] == 'declarations':
                    for declaration in node[1]:
                        var_name = declaration[1]
                        k = declaration[-1]
                        dec = proc.declarations

                        if (var_name in dec.keys()) or (var_name in proc.arg_map.keys()):
                            error(f"Line: {k} name '{var_name}' already used")
                        else:
                            if declaration[0] == 'var':
                                var = Variable(var_name, 'var', proc_name)
                                dec[var_name] = var

                            else:
                                size = declaration[2]
                                var = Variable(var_name, 'array_with_pid', proc_name, size=size)
                                dec[var_name] = var
            for line in procedure:  # analiza komend
                if type(line) is int:
                    continue

                if line[0] == 'commands':
                    for command in line[1]:
                        self.analyze_c(command, proc.declarations, True, proc_name, proc.arg_map, proc.arg_list)
        for node in AST[1]:  # dla maina
            if node[0] == 'declarations':
                for declaration in node[1]:
                    k = declaration[-1]
                    var_name = declaration[1]

                    if var_name in self.main_declarations.keys():
                        error(f"Line: {k} name '{var_name}' already used")
                    if declaration[0] == 'array_with_pid':
                        size = declaration[2]
                        var = Variable(var_name, 'array_with_pid', 'MAIN', size=size)
                        self.main_declarations[var_name] = var
                    else:
                        var = Variable(var_name, 'var', 'MAIN')
                        self.main_declarations[var_name] = var

        for node in AST[1]:

            if node[0] == 'commands':
                for command in node[1]:
                    self.analyze_c(command, self.main_declarations)

    def freeReg(self, reg):
        self.fixed_registers.add(reg)
        if reg in self.free_registers:
            self.free_registers.remove(reg)

    def analyze_c(self, command, declarations, is_proc=False, proc_name=None, arg_map=None, arg_list=None):
        k = command[-1]
        com_type = command[0]
        if com_type == 'ASSIGN':
            i = command[1]

            if i[1] not in declarations.keys():
                if (is_proc and i[1] not in arg_map.keys()) or (not is_proc):
                    error(f"Line: {k} '{i[1]}' is not declared")

            if (i[1] in declarations.keys()) and declarations[i[1]].type == 'var':
                declarations[i[1]].is_Assigned = True

            if is_proc and (i[1] in arg_map.keys()):
                arg_map[i[1]].is_assigning = True

            self.check(k, i, declarations, is_proc, arg_map)
            exp = command[2]

            if exp[0] == 'val':
                val = exp[1]
                self.check_v(k, val, declarations, is_proc, arg_map)

            operator = exp[0]
            if operator == 'ADD' or operator == 'SUB' or operator == 'MUL' or operator == 'DIV' or operator == 'MOD':
                val1 = exp[1]
                val2 = exp[2]

                self.check_v(k, val1, declarations, is_proc, arg_map)
                self.check_v(k, val2, declarations, is_proc, arg_map)

            if operator == 'MUL' or operator == 'DIV':
                self.freeReg("g")
                self.freeReg("e")

        if com_type in {'IF', 'IFELSE', 'WHILE', 'REPEAT'}:

            condition = command[1]
            val1 = condition[1]
            val2 = condition[2]

            if com_type != 'REPEAT':
                self.check_v(k, val1, declarations, is_proc, arg_map)
                self.check_v(k, val2, declarations, is_proc, arg_map)

            if condition[1] == 'EQ' or condition[1] == 'NEQ':
                self.freeReg("g")
                self.freeReg("e")

            if com_type == 'IF':
                if_commands = command[2][1]

                for com in if_commands:
                    self.analyze_c(com, declarations, is_proc, proc_name, arg_map, arg_list)

            if com_type == 'IFELSE':
                if_commands = command[2][1]
                else_commands = command[3][1]

                for com in if_commands:
                    self.analyze_c(com, declarations, is_proc, proc_name, arg_map, arg_list)

                for com in else_commands:
                    self.analyze_c(com, declarations, is_proc, proc_name, arg_map, arg_list)

            if com_type == 'WHILE':
                while_commands = command[2][1]

                for com in while_commands:
                    self.analyze_c(com, declarations, is_proc, proc_name, arg_map, arg_list)

            if com_type == 'REPEAT':
                repeat_commands = command[2][1]

                for com in repeat_commands:
                    self.analyze_c(com, declarations, is_proc, proc_name, arg_map, arg_list)
                self.check_v(k, val1, declarations, is_proc, arg_map)
                self.check_v(k, val2, declarations, is_proc, arg_map)

        if com_type == 'READ':
            i = command[1]

            if i[0] == 'var':
                if (i[1] in declarations.keys()) and declarations[i[1]].type == 'var':
                    declarations[i[1]].is_Assigned = True

            self.check(k, i, declarations, is_proc, arg_map)

        if com_type == 'WRITE':
            val = command[1]
            self.check_v(k, val, declarations, is_proc, arg_map)

        if com_type == 'proc_call':
            c_proc_name = command[1]
            args = command[2]

            if c_proc_name not in self.proc_declarations.keys():
                error(f"Line: {k} Procedure '{c_proc_name}' is not declared")

            amount_proc_args = self.proc_declarations[c_proc_name].arg_list

            if c_proc_name in self.proc_declarations.keys():
                self.proc_declarations[c_proc_name].inc_call_num()

            if len(args) != len(amount_proc_args):
                error(f"Line: {k} wrong amount of arguments")

            for i, arg in enumerate(args):
                if amount_proc_args[i].is_assigning:
                    if arg in declarations.keys():
                        declarations[arg].is_Assigned = True
                    else:
                        arg_map[arg].is_assigning = True

            for i, arg in enumerate(args):
                if arg in declarations.keys() and declarations[arg].type != \
                        self.proc_declarations[c_proc_name].arg_list[i].type:
                    if declarations[arg].type == 'var':
                        error(f"Line: {k}: {arg} wrong type in a procedure")
                    else:
                        error(f"Line: {k}: {arg} isnot a variable")

                if is_proc and arg in arg_map.keys():  # odroznianie argumentow procedury od tej w ktorej jestesmy
                    if arg_map[arg].type != self.proc_declarations[c_proc_name].arg_list[i].type:
                        if arg_map[arg].type == 'var':
                            error(f"Line: {k}: {arg} is not an array")
                        else:
                            error(f"Line: {k}: {arg} is not a variable")

            for arg in args:
                if arg not in declarations and (is_proc and arg not in arg_map or not is_proc):
                    error(f"Line: {k} 'undeclered variable: {arg}'")

    def check_v(self, k, val, declarations, is_proc=False, arguments=None):
        if val[0] == 'i':
            var = val[1]
            self.check(k, var, declarations, is_proc, arguments)

    @staticmethod
    def check(k, i, declarations, is_proc=False, arguments=None):
        if i[0] == 'var':
            if (i[1] in declarations.keys()) and declarations[i[1]].type != 'var':
                error(f"Line: {k} Variable '{i[1]}' wrong usage of an array")
            if is_proc and (i[1] in arguments.keys()) and arguments[i[1]].type != 'var':
                error(f"Line: {k} '{i[1]}' is expected to be an array")
            if i[1] in declarations.keys():
                if not declarations[i[1]].is_Assigned:
                    error(f"Line: {k} '{i[1]}' is expected to be an array")
        if i[1] not in declarations and (is_proc and i[1] not in arguments or not is_proc):
            error(f"Line: {k} Undeclared variable: '{i[1]}'")
        if i[0] == 'array_with_pid' or i[0] == 'array_with_num':
            if (i[1] in declarations.keys()) and declarations[i[1]].type != 'array_with_pid':
                error(f"Line: {k} '{i[1]}' is not declared as an array")
            if is_proc and (i[1] in arguments.keys()) and arguments[i[1]].type != 'array_with_pid':
                error(f"Line: {k} '{i[1]}' is not declared as an array")
            # Check if the index variable is declared
            if (i[2] not in declarations.keys()) and i[0] != 'array_with_num':
                if (is_proc and i[2] not in arguments or not is_proc) and i[1] not in declarations:
                    error(f"Line: {k} Variable '{i[2]}' not declared for array")
            # Check if the index variable is assigned
            if (i[2] in declarations.keys()) and not declarations[i[2]].is_Assigned:  # check A[i] dla i
                error(f"Line: {k} Index variable '{i[2]}' is not assigned for array'")

    def get_data(self):  # ustawia pamiec dla zmiennych w main na poczatku
        for var_name in self.main_declarations.keys():
            var = self.main_declarations[var_name]
            var.set_mem(self.k)
            self.k = self.k + var.size
        for proc_name in self.proc_declarations.keys():
            for var_name in self.proc_declarations[proc_name].declarations.keys():
                var = self.proc_declarations[proc_name].declarations[var_name]
                var.set_mem(self.k)
                self.k = self.k + var.size
        data = (self.proc_declarations, self.main_declarations, self.free_registers)
        return data

    @staticmethod
    def head(head):
        name = head[0]
        args = head[1]
        st = f"{name}("
        for arg in args:
            if arg[0] == 'var':
                st += f"{arg[1]},"
            else:
                st += f"T {arg[1]},"
        st = st[:-1] + ")"
        return st
