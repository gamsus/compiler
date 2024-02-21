#!/bin/bash

# Przykładowe komendy - możesz dostosować je do własnych potrzeb
komendy=("python3 compilator.py ./examples2023/example1.imp ./examples2023_mr/example1.mr"
"python3 compilator.py ./examples2023/example2.imp ./examples2023_mr/example2.mr"
"python3 compilator.py ./examples2023/example3.imp ./examples2023_mr/example3.mr"
"python3 compilator.py ./examples2023/example4.imp ./examples2023_mr/example4.mr"
"python3 compilator.py ./examples2023/example5.imp ./examples2023_mr/example5.mr"
"python3 compilator.py ./examples2023/example6.imp ./examples2023_mr/example6.mr"
"python3 compilator.py ./examples2023/example7.imp ./examples2023_mr/example7.mr"
"python3 compilator.py ./examples2023/example8.imp ./examples2023_mr/example8.mr"
"python3 compilator.py ./examples2023/example9.imp ./examples2023_mr/example9.mr"
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