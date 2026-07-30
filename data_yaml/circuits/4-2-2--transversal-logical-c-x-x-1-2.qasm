OPENQASM 2.0;
include "qelib1.inc";

qreg q[4];

x q[2];
x q[3];
sx q[0];
sx q[1];
sx q[2];
sx q[3];
