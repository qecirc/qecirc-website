OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[13];

z q[8];
z q[4];
z q[3];
z q[2];
y q[10];
x q[7];
x q[11];
y q[5];
cxyz q[9];
cxyz q[12];
sx q[1];
id q[0];
czyx q[8];
czyx q[4];
czyx q[2];
cxyz q[10];
czyx q[7];
cxyz q[11];
swap q[10], q[7];
swap q[9], q[2];
swap q[4], q[12];
swap q[8], q[11];
