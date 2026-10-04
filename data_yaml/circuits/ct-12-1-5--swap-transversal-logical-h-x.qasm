OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[12];

z q[9];
z q[7];
z q[6];
x q[11];
z q[4];
z q[2];
y q[5];
cxyz q[10];
cxyz q[8];
czyx q[3];
czyx q[1];
id q[0];
cxyz q[9];
cxyz q[7];
cxyz q[6];
cxyz q[11];
czyx q[4];
czyx q[2];
czyx q[5];
swap q[3], q[2];
swap q[6], q[11];
swap q[4], q[3];
swap q[7], q[6];
