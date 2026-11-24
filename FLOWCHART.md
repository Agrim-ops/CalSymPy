# CalSymPy: Master Algorithm Flowchart (`FLOWCHART.md`)

> **Course**: MAT 112 Engineering Mathematics & Python Programming  
> **Team 4 (Delta-T)**: Circuit Board Thermal Distribution & Multivariable Calculus  
> **Standard**: ISO / ANSI Standard Flowchart Symbols for Presentation Slides

---

## 1. Flowchart Symbol Guide

| Symbol | Shape | ANSI Meaning | Used In CalSymPy For |
|:---:|:---:|:---|:---|
| **Terminal** | `([ Oval / Pill ])` | Start / Stop | Entry and exit points of the system |
| **Input / Output** | `[/ Parallelogram /]` | Data Input / Output | User inputs (Model, $L$, parameters) & report outputs |
| **Process** | `[ Rectangle ]` | Computational Step | Derivative evaluations, Riemann sums, clamping |
| **Decision** | `{ Diamond }` | Conditional Branching | Model branch (A vs B), critical point check, loop tests |
| **Connector** | `(( Circle ))` | Flow convergence | Merging execution branches |

---

## 2. Mermaid Interactive Flowchart

```mermaid
flowchart TD
    Start([ START ]) --> Input[/ Input: Model A or B, L=4.0 cm, Params, Chip Position x0, y0 /]
    
    Input --> DecModel{ Model == "A"? }
    DecModel -- Yes --> ProcModelA[ "Model A (Gaussian Hotspot):<br>T = T_edge + T0 * exp(-r^2 / s)" ]
    DecModel -- No --> ProcModelB[ "Model B (Sinusoidal Wave):<br>T = T_edge + T0 * sin(pi*x/L) * sin(pi*y/L)" ]
    
    ProcModelA --> MergeModel(( ))
    ProcModelB --> MergeModel
    
    MergeModel --> ProcGrad[ "Compute First Partials & Gradient:<br>Tx = dT/dx, Ty = dT/dy<br>grad T = &lang;Tx, Ty&rang;, ||grad T|| = sqrt(Tx^2 + Ty^2)" ]
    ProcGrad --> ProcHessian[ "Compute Second Partials (Hessian Matrix):<br>Txx = d2T/dx2, Tyy = d2T/dy2, Txy = d2T/dxdy<br>Discriminant D = Txx * Tyy - (Txy)^2" ]
    
    ProcHessian --> DecCrit{ "||grad T|| < 0.01?<br>(Critical Point?)" }
    DecCrit -- No --> NonCrit[ "Not a Critical Point:<br>Gradient != 0, D-Test does not apply" ]
    DecCrit -- Yes --> DecD{ "D > 0 and Txx < 0?" }
    DecD -- Yes --> ClassMax[ "Local Maximum<br>(Hotspot Peak)" ]
    DecD -- No --> DecSaddle{ "D < 0?" }
    DecSaddle -- Yes --> ClassSaddle[ "Saddle Point<br>(Mountain Pass)" ]
    DecSaddle -- No --> ClassOther[ "Local Minimum or Inconclusive" ]
    
    NonCrit --> MergeCalc(( ))
    ClassMax --> MergeCalc
    ClassSaddle --> MergeCalc
    ClassOther --> MergeCalc
    
    MergeCalc --> ProcRiemann[ "Spatial Integration (2D Midpoint Riemann Sum):<br>Discretize plate into 80 x 80 cells (dx = L/80)<br>Total = SUM T(x_mid, y_mid) * dx^2<br>T_avg = Total / L^2" ]
    
    ProcRiemann --> ProcPeak[ "Global Grid Scan (50 x 50):<br>Find Peak Temperature and Coordinates (hx, hy)<br>Evaluate Risk: Low (&lt;70 C), Medium (70-90 C), High (&gt;90 C)<br>Calculate Required Cooling: Drop = Peak - 69.9 C" ]
    
    ProcPeak --> DecChip{ "Is Chip Overheating?<br>T(x0, y0) >= 70 C?" }
    
    DecChip -- No (Safe) --> ChipSafe[ "Chip is Safe:<br>Remain at Initial Position (x0, y0)" ]
    
    DecChip -- Yes (Overheating) --> InitDescent[ "Initialize Downhill Descent:<br>(x, y) = (x0, y0), step = 1" ]
    InitDescent --> LoopDescent{ "step &le; 40 AND<br>||grad T|| &gt; 0?" }
    
    LoopDescent -- Yes --> StepDown[ "Step Downhill:<br>(x, y) = (x, y) - eta * (grad T / ||grad T||)" ]
    StepDown --> ClampStep[ "Enforce Safety Margins:<br>x = clamp(x, 0.2, L - 0.2)<br>y = clamp(y, 0.2, L - 0.2)" ]
    ClampStep --> IncStep[ "Append (x, y) to Path<br>step = step + 1" ]
    IncStep --> LoopDescent
    
    LoopDescent -- No --> PlaceOpt[ "Constrained Proximity Placement:<br>Scan 60 x 60 grid for closest point (x*, y*)<br>satisfying T(x*, y*) &lt; 70 C inside [0.2, L-0.2]" ]
    
    ChipSafe --> MergeEnd(( ))
    PlaceOpt --> MergeEnd
    
    MergeEnd --> Output[/ "Output Results:<br>- Heatmap & Descent Trajectory<br>- Spatial Average T_avg<br>- Peak & Risk Classification<br>- Relocated Safe Coordinate" /]
    Output --> End([ END ])
```

---

## 3. Text-Based Box Flowchart (For PPT Slides & ASCII Diagram)

```text
                  (  START  )
                       |
                       v
         [/ INPUT: Model, L, Params, Chip (x0,y0) /]
                       |
                       v
               < Model == "A"? >
                  /         \
          Yes    /           \   No
                v             v
       [ Model A: Gaussian ]  [ Model B: Sine ]
       [ T = T_edge+T0*e   ]  [ T = T_edge+T0*sin*sin ]
                \             /
                 \           /
                  v         v
                   (   O   )
                       |
                       v
       [ COMPUTE FIRST PARTIALS & GRADIENT ]
       [ Tx = dT/dx,  Ty = dT/dy           ]
       [ grad = <Tx, Ty>,  Mag = sqrt(...) ]
                       |
                       v
       [ COMPUTE HESSIAN & DISCRIMINANT   ]
       [ Txx, Tyy, Txy                     ]
       [ D = Txx*Tyy - (Txy)^2             ]
                       |
                       v
             < Is Mag < 0.01? >
              / (Critical?)  \
       Yes   /                \   No
            v                  v
     < D > 0 & Txx < 0? >   [ Not Critical:      ]
       /          \         [ D-Test N/A         ]
  Yes /            \ No        |
     v              v          |
[ Local Max  ]   < D < 0? >    |
[ (Peak)     ]    /      \     |
     |      Yes  /        \ No |
     |          v          v   |
     |    [ Saddle ]   [ Min / ]
     |    [ Point  ]   [ Incon ]
     \       |         /       /
      \      |        /       /
       v     v       v       v
            (   O   )
                |
                v
       [ 2D RIEMANN SUM (SPATIAL AVERAGE)  ]
       [ Discretize 80x80 Midpoint Cells   ]
       [ T_avg = (1/L^2) * SUM T * dx^2    ]
                |
                v
       [ GLOBAL PEAK & THERMAL RISK        ]
       [ Grid Search 50x50 -> Max T, (hx,hy)]
       [ Risk: Low (<70), Med, High (>90)  ]
       [ Drop Required = Peak - 69.9 C     ]
                |
                v
        < Chip Overheating? (T >= 70 C) >
               /            \
        Yes   /              \   No (Safe)
             v                v
      [ START DESCENT ]    [ Keep Chip at ]
      [ (x,y) = (x0,y0) ]  [ (x0, y0)     ]
             |                    |
             v                    |
     +--> < Step <= 40? >         |
     |       /      \             |
     | Yes  /        \ No         |
     |     v          v           |
     | [ Step Down ] [ SAFE PLACE ]
     | [ Clamp Marg] [ Grid search]
     | [ Step++    ] [ min dist   ]
     +-----+              |       |
                          v       v
                       (   O   )
                           |
                           v
         [/ OUTPUT: Heatmap, T_avg, Peak, /]
         [/ Risk, Relocated Safe Coordinate/]
                           |
                           v
                       (  END  )
```

---

## 4. Slide-Ready 3-Stage Modular Flow (Horizontal Layout)

If your presentation slide is widescreen (16:9), split the flow into 3 consecutive visual stages:

```text
[ STAGE 1: MODELING & CALCULUS ]
( START ) -> [/ Input Params /] -> { Model A or B? } -> [ Evaluate T(x, y) ] 
          -> [ Compute grad T & Magnitude ] -> [ Hessian D-Test ] 
          -> { Critical Point? } -> ( Peak / Saddle / Min )

[ STAGE 2: SPATIAL INTEGRATION & RISK ASSESSMENT ]
( Stage 1 Out ) -> [ 2D Midpoint Riemann Sum (80x80) ] -> [ Calculate Spatial T_avg ]
                -> [ Grid Search 50x50 ] -> [ Find Hottest Point (hx, hy) ]
                -> [ Classify Risk (Low/Med/High) ] -> [ Compute Cooling Drop ]

[ STAGE 3: AUTONOMOUS DOWNHILL RELOCATION & OUTPUT ]
( Stage 2 Out ) -> { Chip Temp >= 70 C? }
                   |-- No  --> [ Keep at Initial Position ]
                   |-- Yes --> [ While step <= 40: Move along -grad T & Clamp Margins ]
                           --> [ Grid Search Closest Safe Point < 70 C ]
                -> [/ Output Heatmap, Average, Risk & Relocation /] -> ( END )
```
