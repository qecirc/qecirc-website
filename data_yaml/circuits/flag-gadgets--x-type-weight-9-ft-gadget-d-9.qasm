OPENQASM 2.0;
include "qelib1.inc";

qreg q[13];
creg rec[4];

h q[0];
cx q[0], q[12];
cx q[0], q[9];
cx q[0], q[8];
cx q[0], q[11];
cx q[0], q[7];
cx q[0], q[6];
cx q[0], q[10];
cx q[0], q[5];
cx q[0], q[12];
cx q[0], q[4];
measure q[12] -> rec[0];
cx q[0], q[3];
cx q[0], q[11];
cx q[0], q[2];
measure q[11] -> rec[1];
cx q[0], q[10];
cx q[0], q[1];
measure q[10] -> rec[2];
cx q[0], q[9];
measure q[9] -> rec[3];
