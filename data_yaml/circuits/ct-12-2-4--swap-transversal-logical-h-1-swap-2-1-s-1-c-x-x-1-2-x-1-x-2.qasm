OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[12];

z q[9];
z q[6];
z q[4];
z q[2];
z q[7];
s q[10];
s q[5];
sx q[11];
czyx q[3];
id q[0];
sx q[9];
h q[6];
h q[4];
cxyz q[2];
swap q[8], q[2];
swap q[3], q[2];
swap q[11], q[8];
swap q[4], q[2];
swap q[5], q[3];
swap q[6], q[8];
swap q[9], q[2];
swap q[10], q[3];
