OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[16];

z q[8];
z q[5];
z q[2];
z q[11];
z q[1];
x q[10];
y q[15];
z q[0];
y q[14];
z q[12];
z q[6];
x q[13];
z q[7];
z q[4];
cxyz q[9];
cxyz q[3];
cxyz q[8];
czyx q[5];
cxyz q[11];
cxyz q[1];
cxyz q[10];
cxyz q[0];
czyx q[14];
czyx q[12];
czyx q[7];
swap q[9], q[3];
swap q[12], q[7];
swap q[0], q[4];
swap q[1], q[10];
swap q[11], q[3];
swap q[14], q[12];
swap q[5], q[0];
swap q[8], q[10];
