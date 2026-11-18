OPENQASM 2.0;
include "qelib1.inc";

qreg q[10];
creg rec[1];

h q[6];
h q[4];
h q[7];
h q[2];
cx q[6], q[8];
cx q[7], q[1];
cx q[4], q[3];
cx q[8], q[0];
cx q[6], q[5];
cx q[3], q[7];
cx q[3], q[0];
cx q[2], q[8];
cx q[4], q[9];
cx q[5], q[9];
cx q[0], q[9];
measure q[9] -> rec[0];
