OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[20];

z q[8];
z q[7];
z q[5];
x q[18];
z q[15];
y q[11];
z q[16];
x q[9];
x q[13];
z q[17];
cxyz q[14];
cxyz q[4];
czyx q[3];
czyx q[12];
czyx q[19];
id q[0];
cxyz q[8];
czyx q[7];
czyx q[5];
cxyz q[15];
cxyz q[11];
cxyz q[9];
czyx q[17];
swap q[18], q[13];
swap q[6], q[16];
swap q[9], q[19];
swap q[11], q[12];
swap q[3], q[15];
swap q[5], q[4];
swap q[8], q[17];
swap q[14], q[7];
