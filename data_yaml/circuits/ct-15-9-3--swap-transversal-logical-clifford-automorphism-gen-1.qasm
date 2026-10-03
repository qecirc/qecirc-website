OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[15];

z q[8];
y q[13];
x q[7];
z q[0];
x q[6];
x q[14];
x q[5];
z q[3];
x q[12];
czyx q[4];
cxyz q[2];
cxyz q[9];
cxyz q[11];
czyx q[8];
cxyz q[7];
czyx q[0];
cxyz q[6];
czyx q[3];
czyx q[12];
swap q[10], q[5];
swap q[11], q[3];
swap q[0], q[6];
swap q[2], q[12];
swap q[4], q[7];
swap q[8], q[9];
