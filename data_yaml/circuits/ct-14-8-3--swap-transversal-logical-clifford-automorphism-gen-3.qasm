OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[14];

z q[8];
z q[9];
x q[13];
z q[11];
z q[3];
x q[5];
z q[2];
y q[4];
cxyz q[7];
cxyz q[12];
czyx q[6];
cxyz q[9];
cxyz q[13];
czyx q[11];
cxyz q[3];
czyx q[5];
czyx q[2];
czyx q[4];
swap q[0], q[6];
swap q[1], q[5];
swap q[9], q[2];
swap q[12], q[6];
swap q[7], q[4];
swap q[13], q[1];
swap q[8], q[2];
swap q[10], q[7];
