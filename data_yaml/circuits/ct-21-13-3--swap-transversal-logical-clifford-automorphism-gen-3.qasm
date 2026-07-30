OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[21];

z q[3];
x q[19];
czyx q[11];
cxyz q[15];
czyx q[2];
cxyz q[9];
czyx q[13];
cxyz q[1];
cxyz q[18];
czyx q[8];
cxyz q[4];
czyx q[5];
swap q[7], q[16];
id q[20];
swap q[1], q[8];
swap q[9], q[5];
swap q[2], q[4];
swap q[15], q[13];
swap q[11], q[18];
