El archivo a ejecutar es "PreciosUnitarios.py".
Consiste en un visor de precios para obras de construcción en Chile (principalmente obras públicas).
Al ejecutarlo, aparece la siguiente interfaz:
<img width="180" height="379" alt="image" src="https://github.com/user-attachments/assets/c70496e2-f86f-4495-952f-c8166961df66" />

Cómo usar:
En el espacio bajo "Ingresar item" señalar alguna partida propia de la construcción. Se puede hacer de las siguientes formas:
a) sólo item: Ej. --> "palmera"  
b) item, unidad: Ej. --> "palmera, un"
c) idem a), pero varios a la vez, Ej. --> "palmera; hormigon pilar"
d) idem b), pero varios a la vez, Ej. --> "palmera, un; hormigon pilar, m3"

Importante: respetar puntuación señalada. Separar item y unidad con "," y varios items con ";".

"Aceptar": presionar una vez escrito item (y unidad opcionalmente)
"Ver precios (todos)": entrega todos los resultados disponibles en la consola, con todas las unidades disponibles (si hubiese más de una)
"Ver precio promedio": en casos b) y d) (cuando se señala la unidad), se muestra el precio promedio en la consola. Cuando hay más de 10 precios parciales
se considera sólo el 70% de ellos, descartando el 30% en los extremos superior/inferior. Para el caso b), adicionalmente, se muestra un esquema gráfico de
estos precios.
Ej: "hormigon pilar, m3"
<img width="478" height="147" alt="image" src="https://github.com/user-attachments/assets/ba1c28f2-189a-47cb-98fa-2c6adbc93052" />

"Ver más información": se muestra todo lo de "Ver precios..." en su versión completa, más otros datos que contribuyen a darle contexto al precio.


