#import  "@preview/dashy-todo:0.1.2": todo
#import "@preview/basic-report:0.5.0": *
#import "@preview/subpar:0.2.2"

#let todo-inline = todo.with(position: "inline", stroke: (paint: red, thickness: 4pt, cap: "round"))

#show: it => basic-report(
  doc-category: "Informe de trabajo práctico 1",
  doc-title: "Simulación de Componentes Fotónicos Pasivos",
  author: "María Luz Stewart Harris",
  affiliation: "Instituto Balseiro",
  language: "es",
  // compact-mode: true,
  it
)

#set math.cases(gap: 0.8em)
#show math.equation.where(block: true): set align(left)
#set heading(numbering: "1.a)")

= Condición de monomodo en guías rectangulares
== Gráfico de índice efectivo versus $W$

#show figure.caption: set text(10pt)

#subpar.grid(
    figure(image("figs/ej1/material_0_neff_vs_width.png"), caption: [
        Material: Silicio ($H$ = 220 nm).
    ]), <fig:ej1_neff_vs_W_Si>,
    figure(image("figs/ej1/material_1_neff_vs_width.png"), caption: [
        Material: Nitruro de silicio ($H$ = 400 nm).
    ]), <fig:ej1_neff_vs_W_SiN>,
    v(3pt),
    caption: [
        $n_"eff"$ en función de $lambda$
    ],
    label: <fig:ej1_neff_vs_W>
)




== Rango de operación monomodo
De la @fig:ej1_neff_vs_W se obtienen los rangos de $W$ que aseguran operación monomodo para $lambda$=1550nm:

#figure(
    table(
        columns: 3,
        [*Plataforma*], [*$W_"min"$ (nm)*],[*$W_"min"$ (nm)*],
        [Si (H=220 nm)], [140],[420],
        [SiN (H=400 nm)], [140],[1100],
    )
)

== Tabla de resultados
#figure(
    table(
        columns: 4,
        [*Plataforma*], [*Modo*],[*$n_"eff"$*], [*$n_g$*],
        [Si (H=220 nm, W=500 nm)], [$"TE"_0$],[2.44],[4.178],
        [Si (H=220 nm, W=500 nm)], [$"TM"_0$],[1.77],[3.72],
        [SiN (H=400 nm, W=500 nm)], [$"TE"_0$],[1.51],[1.825],
        [SiN (H=400 nm, W=500 nm)], [$"TM"_0$],[1.49],[1.77],
    )
)

= Curvas de dispersión
== Curvas de dispersión en la banda C

#subpar.grid(
    figure(image("figs/ej1/material_0_neff_vs_width.png"), caption: [
        Material: Silicio ($H$ = 220 nm).
    ]), <fig:ej1_neff_vs_W_Si>,
    figure(image("figs/ej1/material_1_neff_vs_width.png"), caption: [
        Material: Nitruro de silicio ($H$ = 400 nm).
    ]), <fig:ej1_neff_vs_W_SiN>,
    v(3pt),
    caption: [
        $n_"eff"$ en función de $lambda$
    ],
    label: <fig:ej1_neff_vs_W>
)


#todo-inline([grafico neff vs. lambda])
#todo-inline([grafico ng vs. lambda])
== Ajuste polinomial
#todo-inline([tabla ajuste polinomial deff y ng vs lambda])

= Pérdidas por _mode mismatch_ en curvaturas
== Pérdida por _mode mismatch_ versus radio de curvatura
#todo-inline([graficos perdidas (mm, scattering, total)])

== Radio óptimo de curvatura

#todo-inline([])

== Tabla resumen y discusión
#todo-inline([tabla])
#todo-inline([que plataforma me permite menos area?])

= Divisor de potencia tipo Y-branch

== Geometría y simulación
#todo-inline([])

== Parámetros S
#todo-inline([])

== Análisis de pérdidas
#todo-inline([])

= Acoplador direccional: longitud de _crossover_ vs. _gap_

== Cálculo de modos simétrico y antisimétrico

#todo-inline([grafico E_real en 2D])
#todo-inline([grafico E_real en 1D])

== Longitud de cross-over vs. gap
#todo-inline([tabla ns y na, y Lc resultante (en funcion del gap)])

== Ajuste exponencial
#todo-inline([grafico sim vs ajuste])
#todo-inline([tabla de A, B])


= Diseño de acoplador direccional de 3 dB

== Diseño y optimización
#todo-inline([])

== Resultados de simulación
#todo-inline([grafico |E|^2 vista superior])
#todo-inline([verificacion balance de potenica])
#todo-inline([Parámetros S en funcion de lambda])

== Tabla de resultados
#todo-inline([tabla de resultados])

= Interferómetro Mach-Zehnder

== Implementación de las dos configuraciones
#todo-inline([])

== Respuesta espectral
#todo-inline([])

== FSR versus desbalance
#todo-inline([])