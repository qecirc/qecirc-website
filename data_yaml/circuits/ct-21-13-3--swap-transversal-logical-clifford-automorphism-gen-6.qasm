OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[21];

z q[7];
z q[3];
z q[2];
z q[1];
x q[19];
czyx q[15];
cxyz q[9];
czyx q[12];
cxyz q[4];
czyx q[14];
czyx q[0];
czyx q[17];
cxyz q[5];
cxyz q[20];
swap q[18], q[16];
cxyz q[7];
cxyz q[3];
czyx q[2];
czyx q[19];
cxyz q[1];
swap q[0], q[20];
swap q[4], q[5];
swap q[12], q[17];
swap q[13], q[18];
swap q[9], q[8];
swap q[19], q[12];
swap q[2], q[1];
swap q[15], q[9];
swap q[6], q[20];
swap q[7], q[4];
swap q[11], q[1];
