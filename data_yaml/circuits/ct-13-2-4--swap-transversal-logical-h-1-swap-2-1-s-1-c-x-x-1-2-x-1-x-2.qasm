OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[13];

z q[11];
z q[10];
z q[7];
z q[6];
z q[4];
z q[3];
sx q[5];
s q[12];
cxyz q[9];
id q[0];
s q[11];
sx q[10];
h q[7];
h q[6];
czyx q[3];
swap q[9], q[3];
swap q[4], q[3];
swap q[5], q[9];
swap q[12], q[4];
swap q[6], q[3];
swap q[11], q[9];
swap q[7], q[3];
swap q[10], q[4];
