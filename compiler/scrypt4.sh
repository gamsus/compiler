#!/bin/bash

# Przykładowe komendy - możesz dostosować je do własnych potrzeb
komendy=("./maszynawirtualna/maszyna-wirtualna  ./examples2023_mr/example7.mr"
)

# Wyświetlenie komend przed wykonaniem
echo "Wykonuję komendy w pętli:"

# Pętla wykonująca komendy
for komenda in "${komendy[@]}"
do
  # Dzielenie komendy na słowa i wyświetlanie trzech pierwszych
  echo "Wykonuję: $(echo $komenda | awk '{print $1 $2}')"
  eval $komenda
done

echo "Zakończono wykonanie komend."