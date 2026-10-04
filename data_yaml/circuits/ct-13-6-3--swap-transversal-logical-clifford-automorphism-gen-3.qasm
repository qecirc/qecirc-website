OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[13];

z q[8];
z q[3];
z q[2];
z q[1];
x q[11];
y q[7];
z q[6];
cxyz q[12];
cxyz q[5];
cxyz q[9];
cxyz q[10];
id q[0];
czyx q[8];
cxyz q[3];
cxyz q[2];
cxyz q[1];
cxyz q[11];
cxyz q[7];
cxyz q[6];
swap q[6], q[10];
swap q[12], q[7];
swap q[2], q[9];
swap q[5], q[10];
swap q[1], q[12];
swap q[3], q[9];
