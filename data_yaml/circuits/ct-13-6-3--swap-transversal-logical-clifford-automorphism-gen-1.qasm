OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[13];

z q[8];
z q[4];
z q[2];
x q[12];
x q[11];
z q[7];
x q[9];
y q[6];
x q[10];
czyx q[3];
cxyz q[1];
id q[0];
cxyz q[8];
czyx q[4];
cxyz q[2];
czyx q[12];
czyx q[11];
cxyz q[7];
cxyz q[9];
czyx q[6];
swap q[5], q[10];
swap q[7], q[6];
swap q[11], q[9];
swap q[12], q[5];
swap q[1], q[10];
swap q[4], q[2];
swap q[3], q[11];
swap q[8], q[3];
