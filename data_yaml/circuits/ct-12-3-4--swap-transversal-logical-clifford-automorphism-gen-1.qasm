OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[12];

z q[8];
z q[6];
z q[5];
z q[3];
y q[11];
z q[0];
x q[7];
czyx q[4];
cxyz q[2];
cxyz q[10];
cxyz q[1];
cxyz q[9];
cxyz q[6];
cxyz q[3];
czyx q[11];
cxyz q[0];
cxyz q[7];
swap q[1], q[9];
swap q[0], q[7];
swap q[10], q[9];
swap q[3], q[11];
swap q[6], q[4];
swap q[2], q[0];
swap q[5], q[3];
swap q[8], q[4];
