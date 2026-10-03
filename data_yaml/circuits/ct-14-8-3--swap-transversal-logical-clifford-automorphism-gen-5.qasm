OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[14];

z q[8];
z q[7];
x q[9];
z q[11];
z q[3];
z q[0];
z q[2];
y q[4];
cxyz q[10];
cxyz q[13];
czyx q[1];
czyx q[6];
czyx q[8];
cxyz q[9];
cxyz q[11];
czyx q[3];
cxyz q[0];
czyx q[4];
swap q[1], q[6];
swap q[2], q[4];
swap q[3], q[6];
swap q[13], q[1];
swap q[5], q[4];
swap q[12], q[3];
swap q[7], q[13];
swap q[10], q[2];
swap q[0], q[5];
swap q[8], q[7];
swap q[11], q[0];
swap q[9], q[0];
