OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[14];

z q[10];
z q[9];
x q[13];
z q[6];
z q[5];
z q[4];
x q[7];
sx q[12];
s q[11];
czyx q[3];
id q[0];
h q[10];
czyx q[9];
cxyz q[13];
sx q[6];
s q[5];
h q[4];
swap q[5], q[4];
swap q[6], q[5];
swap q[8], q[4];
swap q[13], q[5];
swap q[9], q[6];
swap q[11], q[8];
swap q[10], q[13];
swap q[12], q[9];
