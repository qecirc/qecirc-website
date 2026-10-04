OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[20];

cxyz q[19];
cxyz q[18];
cxyz q[16];
cxyz q[15];
cxyz q[13];
cxyz q[12];
czyx q[9];
czyx q[8];
czyx q[7];
czyx q[6];
czyx q[5];
swap q[14], q[4];
id q[0];
swap q[8], q[7];
swap q[10], q[5];
swap q[11], q[6];
swap q[16], q[12];
swap q[17], q[14];
swap q[9], q[8];
swap q[15], q[6];
swap q[18], q[5];
swap q[19], q[16];
