OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }

qreg q[15];

z q[10];
z q[8];
z q[6];
z q[13];
z q[5];
z q[4];
y q[11];
y q[9];
cxyz q[7];
cxyz q[14];
id q[0];
cxyz q[10];
cxyz q[8];
cxyz q[6];
cxyz q[13];
swap q[11], q[9];
swap q[4], q[3];
swap q[12], q[4];
swap q[5], q[11];
swap q[14], q[6];
swap q[7], q[13];
swap q[8], q[13];
swap q[10], q[6];
