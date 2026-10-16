# Simulación y análisis — sala de cómputo

300 jornadas de 480 min (≈114 solicitudes por jornada), un técnico, utilización ≈ 91 %.
Niveles: ALTA 15 %, MEDIA 50 %, BAJA 35 %. Las tres estrategias reciben las mismas solicitudes en cada jornada.
Se ejecuta con `python simulacion.py`.

## Tabla principal

| Estrategia | Espera media (min) | Peor espera, promedio (min) | Peor espera, máximo (min) |
|---|---|---|---|
| FIFO | 13.0 | 35.5 | 92.7 |
| Prioridad sin envejecimiento | 13.1 | 77.7 | 243.6 |
| Prioridad con envejecimiento (15 min) | 13.0 | 38.3 | 92.7 |

## Detalle por nivel

| Estrategia | Nivel | Espera media (min) | Peor espera, promedio (min) |
|---|---|---|---|
| FIFO | alta | 13.0 | 30.4 |
| FIFO | media | 13.0 | 34.3 |
| FIFO | baja | 13.1 | 33.1 |
| Prioridad sin envejecimiento | alta | 2.2 | 5.9 |
| Prioridad sin envejecimiento | media | 5.1 | 18.8 |
| Prioridad sin envejecimiento | baja | 29.5 | 77.7 |
| Prioridad con envejecimiento (15 min) | alta | 8.1 | 24.7 |
| Prioridad con envejecimiento (15 min) | media | 12.0 | 33.7 |
| Prioridad con envejecimiento (15 min) | baja | 16.7 | 37.3 |

## Sensibilidad al intervalo de envejecimiento

| Intervalo (min) | Espera media | Peor espera (promedio) | Peor espera BAJA (promedio) |
|---|---|---|---|
| 5 | 13.0 | 35.6 | 33.2 |
| 10 | 13.1 | 36.1 | 34.4 |
| 15 | 13.0 | 38.3 | 37.3 |
| 30 | 13.1 | 46.2 | 46.0 |
| 60 | 13.0 | 59.5 | 59.4 |

## Interpretación

1. **La media no distingue las estrategias.** Las tres dan ≈ 13 min. Es lógico: el técnico nunca queda ocioso
   mientras hay cola y el servicio no depende del nivel, así que la prioridad solo *reparte* la espera, no la
   reduce. Quien mire solo la media concluiría que da igual cuál se use.
2. **El peor caso sí las distingue, y es donde la prioridad pura sale peor.** Sin envejecimiento, la peor
   espera promedio sube de 35.5 (FIFO) a 77.7 min, y en la peor jornada a 243.6 min (≈ 4 h): las solicitudes BAJA
   quedan relegadas mientras lleguen ALTA y MEDIA. Es la espera indefinida del enunciado, observada.
3. **Qué compra la prioridad.** A las ALTA las atiende en 2.2 min de media (frente a 13.0 en FIFO) y a las MEDIA
   en 5.1. Ese beneficio lo pagan las BAJA (29.5 min de media).
4. **El envejecimiento recupera el peor caso casi al nivel de FIFO** (38.3 frente a 35.5; máximo 92.7 en ambos)
   y conserva parte del beneficio: las ALTA bajan de 13.0 a 8.1 min. El costo es que las ALTA ya no esperan
   2.2 min sino 8.1: se cede parte del privilegio a cambio de acotar la espera de las BAJA (de 77.7 a 37.3 min
   de peor caso).
5. **El intervalo es la perilla del compromiso.** Con 5 min el peor caso es casi el de FIFO (35.6) y con 60 min
   crece a 59.5. Un intervalo corto hace que las BAJA suban rápido, lo que cuida su espera pero le quita
   ventaja a la prioridad; un intervalo largo hace lo contrario. En la sala conviene un valor intermedio
   (10–15 min). El valor depende de cuánta espera es tolerable para una solicitud BAJA: es una decisión de
   política, no matemática.

**Limitaciones:** un solo técnico, servicio independiente del nivel, llegadas sin picos (en la realidad hay
más tráfico antes de una entrega). Con picos, el contraste en el peor caso sería probablemente mayor.