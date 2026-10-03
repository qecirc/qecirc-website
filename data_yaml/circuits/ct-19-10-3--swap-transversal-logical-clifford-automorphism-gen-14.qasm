OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[19];

z q[11];
z q[14];
z q[4];
x q[13];
z q[3];
x q[17];
czyx q[5];
cxyz q[18];
cxyz q[12];
cxyz q[15];
czyx q[6];
czyx q[10];
czyx q[7];
id q[0];
cxyz q[11];
czyx q[4];
cxyz q[3];
swap q[6], q[10];
swap q[15], q[7];
swap q[18], q[9];
swap q[3], q[12];
swap q[4], q[10];
swap q[14], q[15];
swap q[5], q[18];
swap q[11], q[12];
