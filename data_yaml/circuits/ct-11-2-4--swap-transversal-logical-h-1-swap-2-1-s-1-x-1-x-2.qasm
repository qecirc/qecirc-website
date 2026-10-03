OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[11];

z q[4];
x q[10];
y q[7];
s q[9];
sx q[8];
h q[5];
czyx q[3];
h q[2];
sx q[1];
id q[0];
cxyz q[10];
s q[7];
swap q[5], q[2];
swap q[8], q[1];
swap q[3], q[10];
swap q[9], q[7];
