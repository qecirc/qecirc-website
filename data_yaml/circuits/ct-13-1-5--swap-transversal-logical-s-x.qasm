OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[13];

z q[4];
x q[6];
s q[11];
h q[10];
sx q[9];
czyx q[8];
cxyz q[12];
s q[5];
sx q[3];
czyx q[2];
id q[0];
h q[4];
swap q[4], q[3];
swap q[5], q[4];
swap q[12], q[3];
swap q[7], q[5];
swap q[8], q[4];
swap q[11], q[12];
swap q[9], q[7];
swap q[10], q[8];
