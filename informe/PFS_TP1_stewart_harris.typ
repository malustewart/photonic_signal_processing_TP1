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
#show figure.caption: set text(10pt)
#show figure.where(kind: image, caption: none): it => {
  counter(figure.where(kind: image)).update(v => v - 1)
  // it.body
  it
}
#show math.equation.where(block: true): eq => {
  block(width: 100%, inset: 0pt, align(center, eq))
}
#let appendix(body) = {
  set heading(numbering: "A", supplement: [Apéndice])
  counter(heading).update(0)
  body
}

= Condición de monomodo en guías rectangulares

Para determinar la condición monomodo en guías rectangulares, se obtiene mediante simulación la relación entre $n_"eff"$ y $W$ para múltiples modos.

Se simulan guías de silicio (Si, con alto de guía $H$=220nm) y nitruro de silicio (SiN, con $H$=400nm).

== Gráfico de índice efectivo versus $W$

Para un barrido de anchos de guía $W$ de entre $0.14 mu m$  y $2.0 mu  m$ se busca el $n_"eff"$ de 10 modos. De estos 10 modos, se compara su $n_"eff"$ con $n_"SiO"_2 = 1.444$, y se descartan aquellos que no cumplan que $n_"eff" >= n_"SiO"_2$ dado a que no son modos guiados. La @fig:ej1_neff_vs_W muestra $n_"eff"$ en función de $W$ para los diferentes modos guiados.

La longitud de onda utilizada para la simulación es $lambda=1550 "nm"$.

#subpar.grid(
    figure(image("figs/ej1/material_0_neff_vs_width.png"), caption: [
        Silicio ($H$ = 220 nm).
    ]), <fig:ej1_neff_vs_W_Si>,
    figure(image("figs/ej1/material_1_neff_vs_width.png"), caption: [
        Nitruro de silicio ($H$ = 400 nm).
    ]), <fig:ej1_neff_vs_W_SiN>,
    v(3pt),
    caption: [
        $n_"eff"$ en función de $W$
    ],
    label: <fig:ej1_neff_vs_W>
)

== Rango de operación monomodo
De la @fig:ej1_neff_vs_W se obtienen los rangos de $W$ que aseguran operación monomodo para $lambda$=1550nm:

#figure(
    table(
        columns: 4,
        [*Plataforma*], [*$W_"min"$ (nm)*],[*$W_"max"$ (nm)*],
        [Si (H=220 nm)], [140],[420],
        [SiN (H=400 nm)], [140],[1100],
    )
)

== Tabla de resultados
De la @fig:ej1_neff_vs_W se obtienen los índices $n_"eff"$ y $n_g$ para los modos fundamentales.

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

Se analiza la dispersión en función de $lambda$ para guías monomodo de silicio y nitruro de silicio.

== Curvas de dispersión en la banda C

#subpar.grid(
    figure(image("figs/ej2/neff_vs_wavelength.png"), caption: [
        $n_"eff"$  vs. $lambda$.
    ]), <fig:ej2_n_vs_lambda_neff>,
    figure(image("figs/ej2/ng_vs_wavelength.png"), caption: [
        $n_g$ vs. $lambda$.
    ]), <fig:ej2_n_vs_lambda_ng>,
    v(3pt),
    caption: [
        $n_"eff"$ y $n_g$ vs. $lambda$ para modos $"TE"_0$, $"TM"_0$, en guías de Si y SiN.
    ],
    label: <fig:ej2_n_vs_lambda>
)



== Ajuste polinomial

La @tab:ej2_polyfit muestra el ajuste polinomial de $n_"eff" (lambda-lambda_0)$ y $n_g (lambda - lambda_0)$ todos los casos se utilizó un ajuste de orden 2:

$
    n(lambda) = a_0 + a_1 (lambda - lambda_0) + a_2 (lambda - lambda_0)^2, quad lambda_0 = 1550"nm"
$

#figure(
    table(
        columns: 7,

        [*Plataforma*],
        [*Modo*],
        [*Magnitud*],
        [*$a_0$*],
        [*$a_1$*],
        [*$a_2$*],
        [*nmse*],

        [Si],
        [$"TE"_0$],
        [$n_"eff" (lambda)$],
        [$1.8255$],
        [$-1.4448$],
        [$1.50499$],
        [$7.0 dot 10^(-10)$],

        [Si],
        [$"TE"_0$],
        [$n_g (lambda)$],
        [$4.0687$],
        [$-4.6510$],
        [$-9.2654$],
        [$2.8269 dot 10^(-8)$],

        [Si],
        [$"TM"_0$],
        [$n_"eff" (lambda)$],
        [$1.5934$],
        [$-0.8126$],
        [$1.9785$],
        [$1.6 dot 10^(-9)$],

        [Si],
        [$"TM"_0$],
        [$n_g (lambda)$],
        [$2.8470$],
        [$-6.1234$],
        [$9.1152$],
        [$1.6 dot 10^(-8)$],

        [SiN],
        [$"TE"_0$],
        [$n_"eff" (lambda)$],
        [$1.5871$],
        [$-0.2702$],
        [$0.1415$],
        [$9.8dot 10 ^(-12)$],

        [SiN],
        [$"TE"_0$],
        [$n_g (lambda)$],
        [$2.0061$],
        [$-0.4475$],
        [$-0.3029$],
        [$1.6 dot 10^(-11)$],

        [SiN],
        [$"TM"_0$],
        [$n_"eff" (lambda)$],
        [$1.5395$],
        [$-0.2303$],
        [$0.2007$],
        [$5.1dot 10^(-13)$],

        [SiN],
        [$"TM"_0$],
        [$n_g (lambda)$],
        [$1.8964$],
        [$-0.6219$],
        [$-0.0165$],
        [$4.9dot 10^(-11)$],
    ),
    caption: []
)<tab:ej2_polyfit>


En la sección @sec:ej2_graficos_disp se grafican los ajustes polinomiales de $n_"eff" (lambda)$ y $n_g (lambda)$ comparados con los valores simulados.

= Pérdidas por _mode mismatch_ en curvaturas
== Pérdida por _mode mismatch_ versus radio de curvatura
Se calculan las pérdidas en una curva de 90° para un barrido de radio de curvatura de entre $2 mu m$ y $120 mu m$. Se calculan las pérdidas por _mode mismatch_ y por propagación (por _scattering_):

$
  L_"MM" = -10 log("overlapping"^2)\
  L_"scattering" = alpha R pi/2 
$

Para calcular la pérdida total, se suman las pérdidas por propagación en la curva con las pérdidas por _mode mismatch_ en ambos extremos de la curva:

$
  L_"total" = 2 dot L_"MM" + L_"scattering"
$

La @fig:ej3_loss_vs_R muestra las pérdidas en función del radio de curvatura.#footnote[Solo se grafican los radios de curvatura donde se encontraron modos guiados.]

#subpar.grid(
    figure(image("figs/ej3/material_0_loss_vs_radius.png", width: 90%), caption: [
        Silicio ($W$=300nm, $H$=220nm).
    ]),
    figure(image("figs/ej3/material_1_loss_vs_radius.png", width: 90%), caption: [
        Nitruro de silicio ($W$=750nm, $H$=400nm).
    ]),
    v(3pt),
    caption: [
        Pérdidas en curva de 90° en función del radio de curvatura para modo $"TE"_0$. 
    ],
    label: <fig:ej3_loss_vs_R>
)

== Tabla resumen y discusión

La @tab:ej3_r_opt muestra el radio óptimo que minimiza las pérdidas de curvatura.

#figure(
    table(
        columns: 3,
        [*Plataforma*], [*$R_"opt"$ ($mu$m)*],[*$L_"min"$ (dB/curva 90°)*],
        [Si], [19.15],[0.016],
        [SiN], [90.48],[0.024],
    )
)<tab:ej3_r_opt>

Al tener un $R_"opt"$ menor con $L_"min"$ menor, la plataforma de silicio permite circuitos con menor área mínima.

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


#show: appendix 

= Gráficos ajuste polinomial de $n_"eff"$ y $n_g$ <sec:ej2_graficos_disp>

#subpar.grid(
    figure(image("figs/ej2/material_0_neff_ng_vs_wavelength_TE0_TM0.TE0_neff.png"), caption: [
        Silicio.
    ]),
    figure(image("figs/ej2/material_1_neff_ng_vs_wavelength_TE0_TM0.TE0_neff.png"), caption: [
        Nitruro de silicio.
    ]),
    v(3pt),
    caption: [
        $n_"eff"$ simulado y ajuste polinomial de n=1 hasta n=4 para modo $"TE"_0$.
    ],
    label: <fig:ej2_neff_TE0_polyfit>
)

#subpar.grid(
    figure(image("figs/ej2/material_0_neff_ng_vs_wavelength_TE0_TM0.TE0_ng.png"), caption: [
        Silicio.
    ]),
    figure(image("figs/ej2/material_1_neff_ng_vs_wavelength_TE0_TM0.TE0_ng.png"), caption: [
        Nitruro de silicio.
    ]),
    v(3pt),
    caption: [
        $n_g$ simulado y ajuste polinomial de n=1 hasta n=4 para modo $"TE"_0$.
    ],
    label: <fig:ej2_ng_TE0_polyfit>
)

#subpar.grid(
    figure(image("figs/ej2/material_0_neff_ng_vs_wavelength_TE0_TM0.TM0_neff.png"), caption: [
        Silicio.
    ]),
    figure(image("figs/ej2/material_1_neff_ng_vs_wavelength_TE0_TM0.TM0_neff.png"), caption: [
        Nitruro de silicio.
    ]),
    v(3pt),
    caption: [
        $n_"eff"$ simulado y ajuste polinomial de n=1 hasta n=4 para modo $"TM"_0$.
    ],
    label: <fig:ej2_neff_TM0_polyfit>
)

#subpar.grid(
    figure(image("figs/ej2/material_0_neff_ng_vs_wavelength_TE0_TM0.TM0_ng.png"), caption: [
        Silicio.
    ]),
    figure(image("figs/ej2/material_1_neff_ng_vs_wavelength_TE0_TM0.TM0_ng.png"), caption: [
        Nitruro de silicio.
    ]),
    v(3pt),
    caption: [
        $n_g$ simulado y ajuste polinomial de n=1 hasta n=4.
    ],
    label: <fig:ej2_ng_TM0_polyfit>
)