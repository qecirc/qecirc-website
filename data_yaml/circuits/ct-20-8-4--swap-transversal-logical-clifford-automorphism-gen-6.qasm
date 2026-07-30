OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[20];

z q[10];
z q[6];
z q[5];
z q[3];
y q[14];
x q[17];
y q[11];
y q[13];
y q[19];
z q[9];
z q[16];
y q[18];
czyx q[15];
cxyz q[12];
cxyz q[4];
id q[0];
czyx q[6];
czyx q[5];
cxyz q[3];
cxyz q[14];
cxyz q[17];
czyx q[11];
czyx q[13];
cxyz q[18];
swap q[19], q[9];
swap q[13], q[18];
swap q[3], q[14];
swap q[5], q[17];
swap q[6], q[11];
swap q[7], q[19];
swap q[8], q[5];
swap q[10], q[13];
swap q[12], q[3];
swap q[15], q[6];
