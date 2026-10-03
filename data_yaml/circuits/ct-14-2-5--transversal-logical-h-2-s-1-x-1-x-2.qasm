OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[14];

z q[12];
z q[10];
z q[9];
z q[6];
z q[3];
z q[2];
z q[1];
z q[0];
y q[13];
z q[11];
czyx q[8];
cxyz q[7];
cxyz q[5];
czyx q[4];
cxyz q[12];
czyx q[10];
cxyz q[9];
czyx q[6];
cxyz q[3];
czyx q[2];
cxyz q[1];
czyx q[0];
cxyz q[13];
czyx q[11];
