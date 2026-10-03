OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[11];

z q[8];
z q[3];
x q[9];
z q[10];
y q[7];
czyx q[2];
czyx q[1];
cxyz q[4];
czyx q[6];
id q[0];
czyx q[8];
cxyz q[3];
cxyz q[9];
cxyz q[7];
swap q[4], q[6];
swap q[2], q[7];
swap q[3], q[1];
swap q[8], q[9];
