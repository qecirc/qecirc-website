OPENQASM 2.0;
include "qelib1.inc";

qreg q[10];
creg rec[3];

h q[6];
h q[4];
h q[2];
cx q[6], q[7];
cx q[2], q[9];
cx q[4], q[8];
cx q[6], q[0];
cx q[6], q[1];
cx q[2], q[0];
cx q[6], q[3];
cx q[2], q[5];
cx q[6], q[7];
cx q[2], q[3];
cx q[4], q[5];
measure q[7] -> rec[0];
cx q[2], q[9];
cx q[4], q[0];
measure q[9] -> rec[1];
cx q[4], q[1];
cx q[4], q[8];
measure q[8] -> rec[2];
