TITLE sodium m3 Brette point
 
COMMENT
Sodium conductance point process with m^3
Based on the publication by Romain Brette "Sharpness of Spike Initiation in Neurons Explained by
Compartmentalization" Plos Computational Biology, 2013.

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
	POINT_PROCESS NavM3Point
	USEION na READ ena WRITE ina
        RANGE gnabar, gna, ena, v_resting, trigger
        RANGE minf, mtau, v1_2
}

PARAMETER {
        gnabar = .12 (uS)	<0,1e9>
	trigger = 0
	mtau = .1 (ms)
	v1_2 = -40 (mV)
        ka = 6 (mV)
	v_resting = -75 (mV)
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
}
 
BREAKPOINT {
        SOLVE states METHOD cnexp
        gna = gnabar*m^3 : changed to m^3
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
        TABLE minf FROM -150 TO 50 WITH 2000
        minf = 1 / (1 + exp((v1_2 - v)/ka))
}
 
NET_RECEIVE (w) {
    trigger = 1
    rates(v_resting)
    m = minf
}
