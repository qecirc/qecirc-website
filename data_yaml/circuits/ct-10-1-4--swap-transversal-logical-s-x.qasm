OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[10];

z q[8];
z q[4];
z q[3];
x q[6];
z q[1];
s q[7];
h q[5];
sx q[2];
cxyz q[0];
sx q[8];
cxyz q[4];
czyx q[3];
s q[6];
h q[1];
swap q[6], q[1];
swap q[2], q[6];
swap q[3], q[1];
swap q[9], q[6];
swap q[4], q[2];
swap q[5], q[3];
swap q[7], q[4];
swap q[8], q[9];
