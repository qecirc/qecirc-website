OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[15];

z q[8];
z q[4];
z q[2];
x q[10];
y q[13];
x q[7];
z q[0];
y q[6];
z q[14];
x q[9];
z q[5];
z q[3];
y q[12];
czyx q[1];
cxyz q[11];
cxyz q[8];
cxyz q[4];
cxyz q[2];
cxyz q[10];
cxyz q[13];
czyx q[7];
cxyz q[6];
cxyz q[14];
czyx q[9];
cxyz q[5];
swap q[5], q[12];
swap q[14], q[11];
swap q[6], q[3];
swap q[9], q[5];
swap q[0], q[6];
swap q[1], q[11];
swap q[10], q[3];
swap q[7], q[9];
swap q[13], q[5];
swap q[2], q[1];
swap q[4], q[6];
swap q[8], q[2];
