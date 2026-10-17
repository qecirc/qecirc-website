OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[10];

z q[8];
x q[9];
x q[6];
z q[5];
sx q[7];
h q[4];
cxyz q[3];
sx q[1];
s q[0];
s q[8];
czyx q[9];
h q[6];
swap q[7], q[1];
swap q[3], q[9];
swap q[4], q[6];
swap q[8], q[0];
