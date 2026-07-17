OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[15];

z q[9];
y q[13];
x q[10];
z q[14];
x q[12];
z q[4];
z q[2];
z q[1];
y q[6];
z q[5];
cxyz q[11];
czyx q[8];
cxyz q[7];
id q[0];
czyx q[9];
czyx q[10];
cxyz q[14];
czyx q[12];
cxyz q[4];
czyx q[2];
cxyz q[1];
cxyz q[6];
czyx q[5];
swap q[6], q[3];
swap q[4], q[7];
swap q[12], q[2];
swap q[13], q[1];
swap q[10], q[2];
swap q[8], q[1];
swap q[9], q[3];
swap q[11], q[4];
