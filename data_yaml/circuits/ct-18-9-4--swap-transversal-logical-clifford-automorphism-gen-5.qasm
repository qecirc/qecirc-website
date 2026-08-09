OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[18];

z q[8];
z q[5];
x q[13];
x q[9];
x q[11];
czyx q[4];
cxyz q[3];
cxyz q[14];
cxyz q[10];
cxyz q[7];
cxyz q[17];
czyx q[15];
id q[0];
cxyz q[5];
czyx q[13];
czyx q[9];
czyx q[11];
swap q[7], q[15];
swap q[16], q[10];
swap q[9], q[14];
swap q[2], q[13];
swap q[4], q[10];
swap q[5], q[11];
swap q[8], q[7];
swap q[1], q[14];
swap q[3], q[13];
swap q[12], q[5];
