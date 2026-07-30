OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }

qreg q[15];

z q[8];
z q[5];
y q[12];
y q[7];
x q[14];
z q[2];
z q[6];
x q[13];
z q[9];
cxyz q[4];
cxyz q[11];
cxyz q[3];
cxyz q[10];
id q[0];
cxyz q[5];
cxyz q[12];
cxyz q[7];
cxyz q[14];
cxyz q[2];
cxyz q[6];
cxyz q[13];
cxyz q[9];
swap q[10], q[9];
swap q[14], q[6];
swap q[7], q[2];
swap q[3], q[13];
swap q[12], q[13];
swap q[11], q[6];
swap q[4], q[9];
swap q[5], q[2];
