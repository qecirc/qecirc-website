OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }

qreg q[14];

z q[4];
z q[3];
y q[11];
z q[2];
x q[6];
z q[13];
z q[1];
y q[5];
x q[12];
z q[8];
cxyz q[10];
cxyz q[9];
id q[0];
cxyz q[4];
cxyz q[3];
cxyz q[11];
cxyz q[2];
cxyz q[6];
cxyz q[13];
cxyz q[1];
cxyz q[5];
cxyz q[12];
cxyz q[8];
swap q[9], q[5];
swap q[13], q[8];
swap q[6], q[12];
swap q[2], q[1];
swap q[11], q[1];
swap q[10], q[8];
swap q[3], q[5];
swap q[4], q[12];
