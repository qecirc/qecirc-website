OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[21];

z q[11];
z q[7];
z q[5];
z q[4];
czyx q[9];
cxyz q[15];
czyx q[14];
czyx q[10];
cxyz q[17];
swap q[6], q[12];
swap q[8], q[20];
id q[0];
cxyz q[11];
czyx q[7];
cxyz q[4];
swap q[10], q[17];
swap q[15], q[14];
swap q[7], q[4];
swap q[11], q[9];
