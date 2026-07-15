OPENQASM 2.0;
include "qelib1.inc";

qreg q[23];

h q[7];
h q[4];
h q[10];
h q[3];
h q[2];
h q[1];
h q[0];
h q[15];
h q[20];
h q[17];
h q[22];
h q[16];
h q[21];
barrier q;

cx q[15], q[8];
cx q[16], q[5];
cx q[17], q[11];
barrier q;

cx q[3], q[15];
cx q[2], q[16];
barrier q;

cx q[7], q[15];
cx q[4], q[16];
cx q[10], q[17];
barrier q;

cx q[3], q[16];
cx q[2], q[17];
barrier q;

cx q[15], q[8];
cx q[16], q[5];
cx q[17], q[11];
barrier q;

cx q[20], q[9];
cx q[21], q[6];
cx q[22], q[12];
barrier q;

cx q[1], q[20];
cx q[0], q[21];
barrier q;

cx q[8], q[20];
cx q[5], q[21];
cx q[11], q[22];
barrier q;

cx q[1], q[21];
cx q[0], q[22];
barrier q;

cx q[20], q[9];
cx q[21], q[6];
cx q[22], q[12];
barrier q;

