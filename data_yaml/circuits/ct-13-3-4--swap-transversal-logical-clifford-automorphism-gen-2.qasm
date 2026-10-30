OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[13];

z q[9];
z q[7];
z q[6];
z q[4];
y q[12];
z q[1];
x q[8];
czyx q[5];
cxyz q[3];
cxyz q[11];
cxyz q[2];
cxyz q[10];
id q[0];
cxyz q[7];
cxyz q[4];
czyx q[12];
cxyz q[1];
cxyz q[8];
swap q[2], q[10];
swap q[1], q[8];
swap q[11], q[10];
swap q[4], q[12];
swap q[7], q[5];
swap q[3], q[1];
swap q[6], q[4];
swap q[9], q[5];
