OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }

qreg q[15];

z q[12];
z q[3];
y q[7];
z q[10];
z q[2];
y q[6];
cxyz q[5];
cxyz q[4];
cxyz q[11];
cxyz q[14];
cxyz q[13];
cxyz q[9];
id q[0];
cxyz q[12];
cxyz q[3];
cxyz q[7];
cxyz q[10];
cxyz q[2];
cxyz q[6];
swap q[4], q[11];
swap q[6], q[9];
swap q[14], q[10];
swap q[5], q[4];
swap q[2], q[9];
swap q[7], q[10];
