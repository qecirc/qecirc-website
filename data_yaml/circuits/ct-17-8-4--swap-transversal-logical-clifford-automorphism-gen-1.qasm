OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[17];

z q[9];
z q[4];
z q[0];
x q[11];
z q[10];
y q[16];
y q[6];
y q[13];
cxyz q[7];
czyx q[5];
czyx q[3];
swap q[2], q[8];
id q[15];
cxyz q[0];
cxyz q[11];
czyx q[10];
czyx q[6];
cxyz q[13];
swap q[4], q[16];
swap q[7], q[5];
swap q[6], q[13];
swap q[11], q[10];
swap q[3], q[0];
