OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[19];

z q[11];
z q[8];
z q[14];
x q[13];
y q[18];
z q[12];
x q[17];
x q[15];
y q[16];
y q[7];
cxyz q[5];
czyx q[4];
cxyz q[9];
czyx q[10];
id q[0];
cxyz q[11];
czyx q[8];
cxyz q[14];
cxyz q[18];
czyx q[12];
cxyz q[17];
cxyz q[15];
cxyz q[16];
czyx q[7];
swap q[16], q[7];
swap q[15], q[10];
swap q[12], q[17];
swap q[6], q[7];
swap q[9], q[16];
swap q[3], q[15];
swap q[18], q[12];
swap q[11], q[10];
swap q[4], q[9];
swap q[14], q[18];
swap q[8], q[3];
swap q[5], q[14];
