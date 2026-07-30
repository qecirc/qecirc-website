OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[15];

z q[12];
z q[11];
x q[14];
x q[8];
h q[13];
sx q[10];
s q[9];
cxyz q[7];
czyx q[6];
cxyz q[4];
id q[0];
s q[12];
sx q[11];
h q[14];
swap q[6], q[5];
swap q[7], q[5];
swap q[9], q[6];
swap q[14], q[7];
swap q[10], q[5];
swap q[12], q[6];
swap q[11], q[7];
swap q[13], q[5];
