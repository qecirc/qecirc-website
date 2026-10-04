OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[22];

z q[17];
z q[11];
z q[9];
z q[8];
z q[6];
z q[5];
cxyz q[19];
czyx q[15];
cxyz q[13];
czyx q[21];
cxyz q[10];
cxyz q[7];
czyx q[12];
cxyz q[20];
czyx q[16];
cxyz q[14];
id q[0];
czyx q[8];
czyx q[5];
swap q[6], q[4];
swap q[7], q[14];
swap q[9], q[18];
swap q[10], q[20];
swap q[5], q[12];
swap q[8], q[16];
swap q[21], q[10];
swap q[13], q[6];
swap q[15], q[7];
swap q[19], q[9];
swap q[11], q[5];
swap q[17], q[8];
