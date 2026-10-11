# IC-8031 — Simulación

<p align="center">
  <img alt="Python" src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white">
  <a href="LICENSE"><img alt="Licencia GPL-3.0" src="https://img.shields.io/github/license/tonys183/IC-8031-Simulacion?style=flat-square&label=Licencia&logo=opensourceinitiative&logoColor=white"></a>
</p>

<p align="center">
  <a href="#temas-generales">Temas generales</a> · <a href="#proyecto-sistema-de-colas-en-un-restaurante-de-comida-rápida">Proyecto</a>
</p>

Tareas y proyecto del curso Simulación (IC-8031), desarrollados en Python. El repositorio reúne ejercicios de probabilidad, generación de números pseudoaleatorios, pruebas estadísticas, distribuciones y simulación de sistemas de colas.

## Temas generales

1. Experimentos aleatorios y estimación de probabilidades.
2. Generación de números pseudoaleatorios.
3. Pruebas estadísticas para evaluar secuencias aleatorias.
4. Generación y análisis de muestras de distribuciones de probabilidad.
5. Sistemas de colas y tiempos de espera.
6. Comparación de configuraciones y análisis de resultados.

## Proyecto (Sistema de colas en un restaurante de comida rápida)

El proyecto consistía en simular la atención de clientes en un restaurante de comida rápida y analizar cómo la cantidad y distribución de equipos afectaban los tiempos de espera y el costo. Se buscaba comparar configuraciones de cajas, freidoras, parrillas de pollo y dispensadoras de refrescos bajo distintos presupuestos y condiciones de demanda, para identificar alternativas que redujeran la espera promedio.

Para resolverlo, se implementó una simulación en Python que genera órdenes y tiempos de servicio, evalúa combinaciones de equipos y registra estadísticas de espera. El proyecto incluye herramientas para generar muestras, comprobar sus distribuciones mediante pruebas de chi-cuadrado y Kolmogorov–Smirnov, y visualizar los resultados. Las configuraciones se comparan a partir de sus costos y métricas para seleccionar las mejores alternativas de atención.
