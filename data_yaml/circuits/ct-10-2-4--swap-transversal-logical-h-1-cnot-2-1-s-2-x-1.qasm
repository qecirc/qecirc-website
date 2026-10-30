OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[10];

z q[8];
z q[7];
z q[2];
x q[9];
z q[1];
y q[6];
sx q[4];
s q[3];
cxyz q[0];
cxyz q[5];
h q[8];
s q[7];
h q[2];
sx q[9];
czyx q[1];
swap q[6], q[0];
swap q[1], q[0];
swap q[3], q[6];
swap q[9], q[0];
swap q[2], q[1];
swap q[4], q[6];
swap q[7], q[0];
swap q[8], q[1];
