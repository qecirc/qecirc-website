OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[20];

z q[12];
z q[7];
z q[3];
x q[14];
z q[13];
y q[19];
y q[9];
y q[16];
cxyz q[10];
czyx q[8];
czyx q[6];
swap q[5], q[11];
id q[0];
cxyz q[3];
cxyz q[14];
czyx q[13];
czyx q[9];
cxyz q[16];
swap q[7], q[19];
swap q[10], q[8];
swap q[9], q[16];
swap q[14], q[13];
swap q[6], q[3];
