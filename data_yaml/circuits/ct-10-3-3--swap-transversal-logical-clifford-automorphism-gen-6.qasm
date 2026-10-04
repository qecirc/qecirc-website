OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }

qreg q[10];

z q[4];
z q[3];
x q[9];
z q[5];
y q[7];
cxyz q[6];
cxyz q[2];
cxyz q[8];
id q[0];
cxyz q[4];
cxyz q[3];
cxyz q[9];
cxyz q[5];
cxyz q[7];
swap q[9], q[7];
swap q[3], q[5];
swap q[4], q[9];
swap q[6], q[3];
