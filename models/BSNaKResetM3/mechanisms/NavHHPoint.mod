TITLE Nav HH Schmidt-Hieber Bischofberge
 
COMMENT
Hodgekin-Huxley type sodium conductance without inhibition as point process.
Based on the publication by Schmidt-Hieber and Bischofberge "Fast Sodium Channel Gating Supports Localized and Efficient Axonal Action Potential Initiation" The Journal of Neuroscienc, 2010.

Author: Bo Hu 2017
Affiliation: Max Planck Institute for Dynamics and Self-Organization, Goettingen
ENDCOMMENT
 
UNITS {
    (mA) = (milliamp)
    (nA) = (nanoamp)
    (mV) = (millivolt)
    (uS) = (microsiemens)
}
 
NEURON {
    POINT_PROCESS NavHHPoint
    USEION na READ ena WRITE ina
    RANGE gnabar, gna, ena, v_resting, trigger
    RANGE minf, mtau, v1_2
}

PARAMETER {
    gnabar = .12 (uS)	<0,1e9>
    trigger = 0
    v_resting = -75 (mV)
    p1 = 136.4 (mV-1ms-1)
    p2 = 113.1 (mV)
    p3 = 19.35 (mV)
    p4 = 0.3593 (ms-1)
    p5 = 25.31 (mV)
}
 
STATE {
    m
}
 
ASSIGNED {
    v (mV)
    ena (mV)
    
    gna (uS)
    ina (nA)
    minf
    mtau (ms)
    alpha (ms-1)
    beta (ms-1)
}
 
BREAKPOINT {
    SOLVE states METHOD cnexp
    gna = gnabar*m
    ina = gna*(v - ena)
}

INITIAL {
    rates(v)
    m = minf
}

DERIVATIVE states {
    rates(v)
    m' =  (minf-m)/mtau
}

PROCEDURE rates(v) {
    TABLE mtau, minf FROM -150 TO 50 WITH 2000
    alpha =  -p1 * (v-p2) / (exp(-(v-p2)/p3) - 1)
    beta = p4 * exp(-v/p5)
    mtau = 1/(alpha+beta)
    minf = alpha*mtau
}

NET_RECEIVE (w) {
    trigger = 1
    rates(v_resting)
    m = minf
}
