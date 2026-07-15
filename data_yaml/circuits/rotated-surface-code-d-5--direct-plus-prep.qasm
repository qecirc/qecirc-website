OPENQASM 2.0;
include "qelib1.inc";

qreg q[25];

h q[15];
h q[5];
h q[8];
h q[2];
h q[21];
h q[7];
h q[1];
h q[22];
h q[10];
h q[6];
h q[0];
h q[11];
h q[24];
barrier q;

cx q[7], q[9];
cx q[1], q[19];
barrier q;

cx q[5], q[9];
cx q[2], q[19];
barrier q;

cx q[15], q[16];
cx q[8], q[9];
cx q[21], q[19];
barrier q;

cx q[10], q[4];
cx q[22], q[12];
barrier q;

cx q[1], q[4];
cx q[7], q[12];
barrier q;

cx q[19], q[20];
cx q[9], q[4];
cx q[16], q[12];
barrier q;

cx q[6], q[23];
cx q[0], q[18];
barrier q;

cx q[22], q[23];
cx q[10], q[18];
barrier q;

cx q[12], q[13];
cx q[4], q[23];
cx q[20], q[18];
barrier q;

cx q[24], q[3];
cx q[11], q[14];
barrier q;

cx q[0], q[3];
cx q[6], q[14];
barrier q;

cx q[18], q[17];
cx q[23], q[3];
cx q[13], q[14];
barrier q;

