OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[16];

z q[5];
z q[3];
z q[11];
z q[14];
z q[2];
x q[8];
y q[7];
y q[15];
z q[10];
z q[12];
x q[6];
x q[4];
y q[13];
czyx q[9];
id q[0];
cxyz q[5];
czyx q[3];
cxyz q[11];
swap q[10], q[13];
swap q[7], q[12];
swap q[8], q[6];
swap q[2], q[15];
swap q[5], q[3];
swap q[9], q[11];
