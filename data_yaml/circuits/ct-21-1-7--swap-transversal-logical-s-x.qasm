OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[21];

cxyz q[18];
cxyz q[17];
cxyz q[15];
cxyz q[14];
czyx q[11];
czyx q[10];
czyx q[9];
czyx q[8];
czyx q[7];
cxyz q[4];
cxyz q[20];
swap q[16], q[12];
id q[0];
swap q[8], q[7];
swap q[10], q[5];
swap q[11], q[6];
swap q[14], q[4];
swap q[19], q[12];
swap q[9], q[7];
swap q[15], q[11];
swap q[17], q[4];
swap q[18], q[10];
