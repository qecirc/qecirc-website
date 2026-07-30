OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[15];

z q[13];
z q[11];
z q[10];
z q[7];
z q[4];
z q[3];
z q[2];
z q[1];
y q[14];
z q[12];
czyx q[9];
cxyz q[8];
cxyz q[6];
czyx q[5];
id q[0];
cxyz q[13];
czyx q[11];
cxyz q[10];
czyx q[7];
cxyz q[4];
czyx q[3];
cxyz q[2];
czyx q[1];
cxyz q[14];
czyx q[12];
