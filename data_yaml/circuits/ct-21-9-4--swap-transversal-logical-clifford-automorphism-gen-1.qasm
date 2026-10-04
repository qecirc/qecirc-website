OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[21];

cxyz q[15];
cxyz q[11];
czyx q[8];
czyx q[5];
czyx q[19];
czyx q[17];
cxyz q[10];
cxyz q[20];
swap q[12], q[13];
swap q[16], q[18];
swap q[6], q[14];
swap q[9], q[7];
id q[0];
swap q[19], q[10];
swap q[8], q[20];
swap q[11], q[5];
swap q[15], q[17];
