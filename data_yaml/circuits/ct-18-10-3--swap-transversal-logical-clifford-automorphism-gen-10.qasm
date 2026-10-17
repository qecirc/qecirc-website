OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[18];

z q[10];
z q[7];
z q[13];
z q[3];
x q[12];
z q[17];
z q[11];
x q[16];
y q[14];
y q[8];
z q[15];
czyx q[5];
cxyz q[9];
cxyz q[6];
id q[0];
cxyz q[10];
czyx q[3];
czyx q[12];
czyx q[17];
cxyz q[14];
czyx q[8];
cxyz q[15];
swap q[15], q[9];
swap q[8], q[6];
swap q[14], q[5];
swap q[11], q[9];
swap q[2], q[14];
swap q[12], q[6];
swap q[7], q[5];
swap q[17], q[11];
swap q[13], q[2];
swap q[4], q[12];
swap q[3], q[11];
swap q[10], q[4];
