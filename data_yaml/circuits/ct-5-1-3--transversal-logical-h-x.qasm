OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }

qreg q[5];

cxyz q[2];
cxyz q[1];
cxyz q[0];
cxyz q[3];
cxyz q[4];
