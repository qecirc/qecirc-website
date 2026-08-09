OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[11];

z q[9];
z q[8];
z q[5];
z q[4];
z q[2];
z q[1];
sx q[3];
s q[10];
cxyz q[7];
id q[0];
s q[9];
sx q[8];
h q[5];
h q[4];
czyx q[1];
swap q[7], q[1];
swap q[2], q[1];
swap q[3], q[7];
swap q[10], q[2];
swap q[4], q[1];
swap q[9], q[7];
swap q[5], q[1];
swap q[8], q[2];
