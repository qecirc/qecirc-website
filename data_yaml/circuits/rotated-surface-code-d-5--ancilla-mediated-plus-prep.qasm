OPENQASM 2.0;
include "qelib1.inc";

qreg q[47];

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
h q[27];
h q[37];
h q[36];
h q[46];
h q[29];
h q[31];
h q[32];
h q[34];
h q[39];
h q[41];
h q[42];
h q[44];
barrier q;

cx q[27], q[16];
cx q[29], q[9];
cx q[31], q[19];
barrier q;

cx q[15], q[27];
cx q[8], q[29];
cx q[21], q[31];
barrier q;

cx q[5], q[29];
cx q[2], q[31];
barrier q;

cx q[7], q[29];
cx q[1], q[31];
barrier q;

cx q[27], q[16];
cx q[29], q[9];
cx q[31], q[19];
barrier q;

cx q[36], q[20];
cx q[34], q[4];
cx q[32], q[12];
barrier q;

cx q[19], q[36];
cx q[9], q[34];
cx q[16], q[32];
barrier q;

cx q[1], q[34];
cx q[7], q[32];
barrier q;

cx q[10], q[34];
cx q[22], q[32];
barrier q;

cx q[36], q[20];
cx q[34], q[4];
cx q[32], q[12];
barrier q;

cx q[37], q[13];
cx q[39], q[23];
cx q[41], q[18];
barrier q;

cx q[12], q[37];
cx q[4], q[39];
cx q[20], q[41];
barrier q;

cx q[22], q[39];
cx q[10], q[41];
barrier q;

cx q[6], q[39];
cx q[0], q[41];
barrier q;

cx q[37], q[13];
cx q[39], q[23];
cx q[41], q[18];
barrier q;

cx q[46], q[17];
cx q[44], q[3];
cx q[42], q[14];
barrier q;

cx q[18], q[46];
cx q[23], q[44];
cx q[13], q[42];
barrier q;

cx q[0], q[44];
cx q[6], q[42];
barrier q;

cx q[24], q[44];
cx q[11], q[42];
barrier q;

cx q[46], q[17];
cx q[44], q[3];
cx q[42], q[14];
barrier q;

