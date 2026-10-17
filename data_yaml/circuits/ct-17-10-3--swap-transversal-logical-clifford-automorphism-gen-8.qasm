OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[17];

x q[11];
x q[16];
z q[1];
x q[13];
x q[14];
z q[5];
cxyz q[9];
cxyz q[6];
czyx q[12];
cxyz q[2];
cxyz q[10];
cxyz q[7];
cxyz q[8];
id q[0];
cxyz q[11];
czyx q[13];
cxyz q[14];
swap q[15], q[5];
swap q[1], q[7];
swap q[2], q[8];
swap q[10], q[13];
swap q[16], q[15];
swap q[11], q[14];
swap q[12], q[7];
swap q[6], q[8];
swap q[3], q[10];
swap q[9], q[11];
