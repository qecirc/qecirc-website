OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[20];

z q[14];
z q[8];
z q[7];
z q[5];
z q[4];
x q[18];
z q[11];
x q[12];
y q[13];
y q[17];
czyx q[10];
czyx q[15];
czyx q[16];
czyx q[9];
id q[0];
cxyz q[8];
czyx q[7];
czyx q[5];
cxyz q[4];
cxyz q[18];
cxyz q[12];
cxyz q[13];
cxyz q[17];
swap q[13], q[17];
swap q[19], q[13];
swap q[12], q[17];
swap q[9], q[19];
swap q[11], q[13];
swap q[15], q[12];
swap q[14], q[17];
swap q[16], q[19];
swap q[3], q[9];
swap q[4], q[13];
swap q[8], q[15];
swap q[18], q[16];
swap q[5], q[19];
swap q[6], q[18];
swap q[10], q[5];
swap q[7], q[18];
