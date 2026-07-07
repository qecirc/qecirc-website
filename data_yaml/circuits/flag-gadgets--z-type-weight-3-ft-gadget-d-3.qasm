OPENQASM 2.0;
include "qelib1.inc";

qreg q[4];
creg rec[1];

h q[3];
cx q[3], q[0];
cx q[2], q[0];
cx q[1], q[0];
cx q[3], q[0];
h q[3];
measure q[3] -> rec[0];
