OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[20];

czyx q[19];
czyx q[16];
cxyz q[14];
cxyz q[13];
czyx q[11];
czyx q[9];
czyx q[8];
cxyz q[6];
cxyz q[5];
cxyz q[18];
id q[0];
swap q[8], q[18];
swap q[9], q[6];
swap q[11], q[5];
swap q[13], q[12];
swap q[14], q[7];
swap q[10], q[6];
swap q[15], q[18];
swap q[16], q[12];
swap q[17], q[11];
swap q[19], q[7];
