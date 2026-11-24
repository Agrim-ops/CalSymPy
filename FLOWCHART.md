# CalSymPy: Flowchart Specification (`FLOWCHART.md`)

> **Course**: MAT 112 Engineering Mathematics & Python Programming  
> **Team 4 (Delta-T)**: Circuit Board Thermal Distribution & Multivariable Calculus  
> **Convention Requested**:
> - **Start / Stop**: Circle / Oval (`([ ... ])`)
> - **Input / Output (I/O)**: Rectangle (`[ ... ]`)
> - **Process (Calculations / Execution)**: Parallelogram (`[/ ... /]`)
> - **Decision**: Diamond (`{ ... }`)

---

## 1. Symbol Mapping Guide

| Symbol Name | Shape | Used in CalSymPy For |
|:---:|:---:|:---|
| **Terminal** | `([ Circle / Oval ])` | `([ START ])` and `([ END ])` |
| **Input / Output (I/O)** | `[ Rectangle ]` | `[ INPUT: Parameters ]` and `[ OUTPUT: Heatmap & Reports ]` |
| **Process / Calculation** | `[/ Parallelogram /]` | `[/ Derivatives, Riemann Sum, Downhill Stepping, Clamping /]` |
| **Decision** | `{ Diamond }` | `{ Model A vs B? }`, `{ Critical Point? }`, `{ Overheating? }` |

---

## 2. Mermaid Interactive Flowchart

```mermaid
flowchart TD
    Start([ START ]) --> Input[ "INPUT: Model A or B, L=4.0 cm, Params, Chip Position (x0, y0)" ]
    
    Input --> DecModel{ Model == "A"? }
    DecModel -- Yes --> ProcModelA[/ "Process Model A:<br>T = T_edge + T0 * exp(-r^2 / s)" /]
    DecModel -- No --> ProcModelB[/ "Process Model B:<br>T = T_edge + T0 * sin(pi*x/L) * sin(pi*y/L)" /]
    
    ProcModelA --> MergeModel(( ))
    ProcModelB --> MergeModel
    
    MergeModel --> ProcGrad[/ "Process First Partials & Gradient:<br>Tx = dT/dx, Ty = dT/dy<br>grad T = &lang;Tx, Ty&rang;, ||grad T|| = sqrt(Tx^2 + Ty^2)" /]
    ProcGrad --> ProcHessian[/ "Process Second Partials & Hessian:<br>Txx = d2T/dx2, Tyy = d2T/dy2, Txy = d2T/dxdy<br>Discriminant D = Txx * Tyy - (Txy)^2" /]
    
    ProcHessian --> DecCrit{ "||grad T|| < 0.01?<br>(Critical Point?)" }
    DecCrit -- No --> NonCrit[/ "Process Note:<br>Gradient != 0, D-Test does not apply" /]
    DecCrit -- Yes --> DecD{ "D > 0 and Txx < 0?" }
    DecD -- Yes --> ClassMax[/ "Process Classification:<br>Local Maximum (Hotspot Peak)" /]
    DecD -- No --> DecSaddle{ "D < 0?" }
    DecSaddle -- Yes --> ClassSaddle[/ "Process Classification:<br>Saddle Point (Mountain Pass)" /]
    DecSaddle -- No --> ClassOther[/ "Process Classification:<br>Local Minimum or Inconclusive" /]
    
    NonCrit --> MergeCalc(( ))
    ClassMax --> MergeCalc
    ClassSaddle --> MergeCalc
    ClassOther --> MergeCalc
    
    MergeCalc --> ProcRiemann[/ "Process Spatial Integration (2D Riemann Sum):<br>Discretize plate into 80 x 80 cells (dx = L/80)<br>Total = SUM T(x_mid, y_mid) * dx^2<br>T_avg = Total / L^2" /]
    
    ProcRiemann --> ProcPeak[/ "Process Global Grid Scan (50 x 50):<br>Find Peak Temperature and Coordinates (hx, hy)<br>Evaluate Risk: Low (&lt;70 C), Medium (70-90 C), High (&gt;90 C)<br>Calculate Required Cooling: Drop = Peak - 69.9 C" /]
    
    ProcPeak --> DecChip{ "Is Chip Overheating?<br>T(x0, y0) >= 70 C?" }
    
    DecChip -- No (Safe) --> ChipSafe[/ "Process Status:<br>Chip is Safe, Remain at (x0, y0)" /]
    
    DecChip -- Yes (Overheating) --> InitDescent[/ "Process Initialize Descent:<br>(x, y) = (x0, y0), step = 1" /]
    InitDescent --> LoopDescent{ "step &le; 40 AND<br>||grad T|| &gt; 0?" }
    
    LoopDescent -- Yes --> StepDown[/ "Process Step Downhill:<br>(x, y) = (x, y) - eta * (grad T / ||grad T||)" /]
    StepDown --> ClampStep[/ "Process Enforce Safety Margins:<br>x = clamp(x, 0.2, L - 0.2)<br>y = clamp(y, 0.2, L - 0.2)" /]
    ClampStep --> IncStep[/ "Process Update:<br>Append (x, y) to Path, step = step + 1" /]
    IncStep --> LoopDescent
    
    LoopDescent -- No --> PlaceOpt[/ "Process Constrained Placement Search:<br>Scan 60 x 60 grid for closest point (x*, y*)<br>satisfying T(x*, y*) &lt; 70 C inside [0.2, L-0.2]" /]
    
    ChipSafe --> MergeEnd(( ))
    PlaceOpt --> MergeEnd
    
    MergeEnd --> Output[ "OUTPUT: Heatmap & Descent Trail, Spatial Average T_avg, Peak & Risk Classification, Safe Relocated Coordinate" ]
    Output --> End([ END ])
```

---

## 3. Visual Text / PPT Shape Diagram

```text
                  ([  START  ])
                       │
                       ▼
       ┌────────────────────────────────────────────────────────┐
       │   INPUT: Model, L, Params (T_edge, T0, s), Chip (x0,y0) │  <-- RECTANGLE (I/O)
       └────────────────────────────────────────────────────────┘
                       │
                       ▼
              { Model == "A"? }                                     <-- DIAMOND (DECISION)
                 /           \
         Yes    /             \    No
               ▼               ▼
      /───────────────────────/  /──────────────────────────/
     /  PROCESS MODEL A:     /  /  PROCESS MODEL B:        /       <-- PARALLELOGRAM (PROCESS)
    /   T = T_edge+T0*exp   /  /   T = T_edge+T0*sin*sin  /
   /───────────────────────/  /──────────────────────────/
               \               /
                \             /
                 ▼           ▼
                      (( ))
                        │
                        ▼
      /─────────────────────────────────────────────────/
     /   PROCESS FIRST PARTIALS & GRADIENT:            /           <-- PARALLELOGRAM (PROCESS)
    /    Tx = dT/dx,  Ty = dT/dy                      /
   /     grad T = <Tx, Ty>,  ||grad T|| = sqrt(...)  /
  /─────────────────────────────────────────────────/
                        │
                        ▼
      /─────────────────────────────────────────────────/
     /   PROCESS HESSIAN MATRIX & DISCRIMINANT:        /           <-- PARALLELOGRAM (PROCESS)
    /    Txx = d2T/dx2,  Tyy = d2T/dy2,  Txy = d2T/dxdy/
   /     D = Txx * Tyy - (Txy)^2                      /
  /─────────────────────────────────────────────────/
                        │
                        ▼
             { Is ||grad|| < 0.01? }                                <-- DIAMOND (DECISION)
             {   (Critical Point?) }
                /             \
        Yes    /               \   No
              ▼                 ▼
      { D > 0 & Txx < 0? }     /───────────────────────/
         /          \         /  PROCESS: Non-Critical/            <-- PARALLELOGRAM (PROCESS)
   Yes  /            \ No    /   D-Test does not apply/
       ▼              ▼     /───────────────────────/
  /────────────/   { D < 0? }           │
 / PROCESS:   /      /    \             │
/  Local Max / Yes  /      \ No         │
/────────────/     ▼        ▼           │
       │     /──────────/ /──────────/  │
       │    / PROCESS: / / PROCESS: /   │
       │   /  Saddle  / / Min/Incon/    │
       │  /──────────/ /──────────/     │
       \          │       /             /
        \         │      /             /
         ▼        ▼     ▼             ▼
                   (( ))
                     │
                     ▼
      /─────────────────────────────────────────────────/
     /   PROCESS 2D MIDPOINT RIEMANN SUM INTEGRAL:     /           <-- PARALLELOGRAM (PROCESS)
    /    Discretize plate into 80 x 80 cells           /
   /     T_avg = (1/L^2) * SUM T(x_mid, y_mid) * dx^2  /
  /─────────────────────────────────────────────────/
                     │
                     ▼
      /─────────────────────────────────────────────────/
     /   PROCESS GLOBAL PEAK & THERMAL RISK SCAN:      /           <-- PARALLELOGRAM (PROCESS)
    /    Grid 50 x 50 -> Max T at (hx, hy)             /
   /     Risk: Low (<70 C), Med, High (>90 C)          /
  /      Required Cooling Drop = Peak - 69.9 C         /
 /─────────────────────────────────────────────────/
                     │
                     ▼
        { Is Chip Overheating? (T >= 70 C) }                        <-- DIAMOND (DECISION)
                 /                 \
         Yes    /                   \   No (Safe)
               ▼                     ▼
      /──────────────────/     /──────────────────────/
     /  PROCESS:        /     /  PROCESS: Chip Safe, /             <-- PARALLELOGRAM (PROCESS)
    /   (x, y)=(x0, y0)/     /   Remain at (x0, y0) /
   /──────────────────/     /──────────────────────/
               │                     │
               ▼                     │
       ┌──►{ Step <= 40? }           │                              <-- DIAMOND (DECISION)
       │      /       \              │
       │Yes  /         \ No          │
       │    ▼           ▼            │
       │ /─────────────────────────/ │
       │/ PROCESS DOWNHILL STEP:  /  │                             <-- PARALLELOGRAM (PROCESS)
       │/ (x, y) -= eta * unit_dir/  │
       │/ Clamp margins [0.2, L-0.2] │
       │/ Path.append, Step++     /  │
       │/─────────────────────────/  │
       └───┘            │            │
                        ▼            │
             /───────────────────────────────/
            /  PROCESS CONSTRAINED SEARCH:  /                      <-- PARALLELOGRAM (PROCESS)
           /   Scan 60x60 grid for closest /
          /    (x*, y*) with T < 70 C     /
         /───────────────────────────────/
                        │            │
                        ▼            ▼
                   (( MERGE ))
                        │
                        ▼
       ┌────────────────────────────────────────────────────────┐
       │   OUTPUT: Heatmap, T_avg, Peak & Risk, Safe Placement   │  <-- RECTANGLE (I/O)
       └────────────────────────────────────────────────────────┘
                        │
                        ▼
                  ([   END   ])
```
