TITLE sodium_brette_point
 
COMMENT
Sodium conductance point process. 
Based on the publication by Romain Brette "Sharpness of Spike Initiation in Neurons Explained by
Compartmentalization" Plos Computational Biology, 2013.

Author: David Hofmann 2014
Affiliation: Max Planck Institute for Dynamics and Self-Organization, Goettingen

Modified by: Bo Hu 2016
Modification:
* Changed units: g (uS), i (nA)
* Changed minf, mtau, v1_2 to range variables
ENDCOMMENT
 
UNITS {
        (mA) = (milliamp)
        (nA) = (nanoamp)
        (mV) = (millivolt)
	(uS) = (microsiemens)
}
 
NEURON {
	POINT_PROCESS Nav_point
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

PROCEDURE rates(v) {:Computes rate and other constants at current v.
                        :Call once from HOC to initialize inf at resting v.
        TABLE minf FROM -150 TO 50 WITH 2000
        minf = 1 / (1 + exp((v1_2 - v)/ka))
}
 
NET_RECEIVE (w) {
    trigger = 1
    rates(v_resting)
    m = minf
}
