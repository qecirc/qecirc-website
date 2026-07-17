OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[20];

z q[15];
z q[19];
z q[8];
z q[5];
z q[4];
z q[2];
z q[10];
y q[18];
y q[14];
y q[12];
czyx q[17];
cxyz q[13];
czyx q[11];
cxyz q[7];
czyx q[6];
czyx q[3];
czyx q[16];
id q[0];
cxyz q[19];
cxyz q[4];
czyx q[2];
cxyz q[18];
cxyz q[12];
swap q[3], q[16];
swap q[5], q[10];
swap q[8], q[14];
swap q[4], q[18];
swap q[6], q[2];
swap q[7], q[12];
swap q[11], q[14];
swap q[13], q[16];
swap q[17], q[10];
swap q[19], q[2];
swap q[9], q[12];
swap q[15], q[18];
