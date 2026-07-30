OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }

qreg q[16];

cxyz q[14];
cxyz q[12];
cxyz q[11];
cxyz q[10];
cxyz q[9];
cxyz q[8];
cxyz q[7];
cxyz q[6];
cxyz q[5];
cxyz q[4];
cxyz q[3];
cxyz q[2];
cxyz q[1];
cxyz q[0];
cxyz q[13];
cxyz q[15];
