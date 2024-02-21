#!/bin/bash

# Przykładowe komendy - możesz dostosować je do własnych potrzeb
komendy=("python3 compilator.py ./examples/error1.imp ./errors/error1.mr"
"python3 compilator.py ./examples/error2.imp ./errors/error2.mr"
"python3 compilator.py ./examples/error3.imp ./errors/error3.mr"
"python3 compilator.py ./examples/error4.imp ./errors/error4.mr"
"python3 compilator.py ./examples/error5.imp ./errors/error5.mr"
"python3 compilator.py ./examples/error6.imp ./errors/error6.mr"
"python3 compilator.py ./examples/error7.imp ./errors/error7.mr"
"python3 compilator.py ./examples/error8.imp ./errors/error8.mr"
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

