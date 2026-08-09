OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[15];

z q[10];
z q[8];
z q[7];
z q[14];
x q[12];
z q[4];
z q[11];
z q[3];
y q[9];
cxyz q[6];
czyx q[13];
id q[0];
cxyz q[8];
czyx q[14];
swap q[3], q[9];
swap q[6], q[13];
swap q[11], q[3];
swap q[12], q[9];
swap q[14], q[13];
swap q[8], q[6];
swap q[4], q[11];
swap q[10], q[8];
