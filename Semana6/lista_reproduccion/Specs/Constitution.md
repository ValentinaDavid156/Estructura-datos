# Constitución del Proyecto

## 1. Misión
Implementar y evaluar una `ListaEnlazada` para el reproductor de una radio universitaria, comparando empírica y teóricamente su desempeño contra `ListaArreglo` para tomar una decisión de arquitectura basada en datos reales de uso.

## 2. Reglas Inviolables 
1. **Contrato Inviolable**: `ListaEnlazada` debe superar la suite de pruebas de la Actividad 2 (`test_lista.py`) **sin modificar una sola línea** de dicho archivo.
2. **Prohibición de Atajos**: Queda estrictamente prohibido usar la estructura `list` nativa de Python internamente dentro de `ListaArreglo` o `ListaEnlazada`. Los enlaces deben ser gestionados mediante objetos `Nodo`.
3. **Decisión Basada en Datos**: La recomendación del reproductor debe derivarse exclusivamente de los cálculos ponderados de frecuencias diarias de la emisora, no de intuiciones generales.
4. **Verificación Estricta de Casos Límite**: `test_extremos.py` debe cubrir de forma aislada e independiente: lista vacía, lista de un solo elemento, borrado del primero y borrado del último.

## 3. Criterios de Calificación 
- Comprensión de referencias de memoria en `nodos_a_mano.md`.
- Cumplimiento del contrato existente en `lista_enlazada.py`.
- Cobertura total de los 4 casos extremos en `test_extremos.py`.
- Análisis teórico vs. medido y cálculo del día operativo en `comparacion.md`.