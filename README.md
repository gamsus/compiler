Compilator of a simple imperative language
How to run the project

    You have to write in terminal: make, which will compile the project.
    When compilation is done the compiler run-file will be created in the folder. Outside build and src folders of course.
    Then type in ./compiler <file_name> <file_output> -> the output of the program will be in the file which name you have given in the second argument. It would be an assembly code of the program after compilation.
    Read.me is in next folder how to compile a compiler and virtual machine.
    You have to compile virtual machine as well.
    Finally, type in ./vm <file_output> to run the program in virtual machine. The output of the program will be in the terminal.

It has all the files which are being created during the compilation of the project. It won't createe automatically so you have to create it manually if you already don't have it, but I included it so you don't have to create it. It is necessary to have this folder, otherwise the project won't compile, since the compilation process creates some files in this folder and then links them with the rest of the project files and makefile will throw that there is no folder like build.
Overview of the project logic

The project is divided into two parts:

    Compiler - it reads the program written in the language and creates an assembly code of the program.
    Virtual machine - it reads the assembly code and runs the program.

Authors
    Michal Baluta - compiler
    Dr Maciej Gębala - virtual machine and assignment
