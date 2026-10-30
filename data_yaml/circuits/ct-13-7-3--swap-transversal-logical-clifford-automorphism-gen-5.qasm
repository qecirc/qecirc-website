OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }

qreg q[13];

x q[9];
y q[10];
x q[5];
z q[12];
z q[4];
x q[11];
z q[7];
cxyz q[3];
cxyz q[2];
cxyz q[1];
cxyz q[8];
cxyz q[0];
cxyz q[9];
cxyz q[10];
cxyz q[5];
cxyz q[12];
cxyz q[4];
cxyz q[11];
cxyz q[7];
swap q[8], q[7];
swap q[12], q[4];
swap q[5], q[0];
swap q[1], q[11];
swap q[10], q[0];
swap q[9], q[7];
swap q[2], q[4];
swap q[3], q[11];
