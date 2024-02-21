#!/bin/bash

# Przykładowe komendy - możesz dostosować je do własnych potrzeb
komendy=("python3 compilator.py ./examples/program0.imp ./examples_mr/program0.mr"
"python3 compilator.py ./examples/program1.imp ./examples_mr/program1.mr"
"python3 compilator.py ./examples/program2.imp ./examples_mr/program2.mr"
"python3 compilator.py ./examples/program3.imp ./examples_mr/program3.mr"
)

# Wyświetlenie komend przed wykonaniem
echo "Wykonuję komendy w pętli:"

# Pętla wykonująca komendy
for komenda in "${komendy[@]}"
do
  # Dzielenie komendy na słowa i wyświetlanie trzech pierwszych
  echo "Wykonuję: $(echo $komenda | awk '{print $1, $2, $3, $4}')"
  eval $komenda
done

echo "Zakończono wykonanie komend."