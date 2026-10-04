OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[21];

z q[11];
z q[7];
z q[3];
z q[2];
x q[19];
cxyz q[15];
czyx q[9];
cxyz q[13];
czyx q[18];
cxyz q[8];
czyx q[12];
czyx q[16];
cxyz q[4];
cxyz q[14];
cxyz q[0];
cxyz q[17];
czyx q[5];
czyx q[10];
id q[20];
cxyz q[11];
czyx q[3];
czyx q[2];
swap q[0], q[10];
swap q[4], q[5];
swap q[12], q[17];
swap q[8], q[16];
swap q[9], q[13];
swap q[15], q[18];
swap q[3], q[14];
swap q[11], q[2];
