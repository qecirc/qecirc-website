OPENQASM 2.0;
include "qelib1.inc";

qreg q[31];

reset q[0];
reset q[1];
reset q[3];
reset q[7];
reset q[15];
reset q[2]; h q[2]; // decomposed RX
reset q[4]; h q[4]; // decomposed RX
reset q[5]; h q[5]; // decomposed RX
reset q[6]; h q[6]; // decomposed RX
reset q[8]; h q[8]; // decomposed RX
reset q[9]; h q[9]; // decomposed RX
reset q[10]; h q[10]; // decomposed RX
reset q[11]; h q[11]; // decomposed RX
reset q[12]; h q[12]; // decomposed RX
reset q[13]; h q[13]; // decomposed RX
reset q[14]; h q[14]; // decomposed RX
reset q[16]; h q[16]; // decomposed RX
reset q[17]; h q[17]; // decomposed RX
reset q[18]; h q[18]; // decomposed RX
reset q[19]; h q[19]; // decomposed RX
reset q[20]; h q[20]; // decomposed RX
reset q[21]; h q[21]; // decomposed RX
reset q[22]; h q[22]; // decomposed RX
reset q[23]; h q[23]; // decomposed RX
reset q[24]; h q[24]; // decomposed RX
reset q[25]; h q[25]; // decomposed RX
reset q[26]; h q[26]; // decomposed RX
reset q[27]; h q[27]; // decomposed RX
reset q[28]; h q[28]; // decomposed RX
reset q[29]; h q[29]; // decomposed RX
reset q[30]; h q[30]; // decomposed RX
cx q[24], q[15];
cx q[13], q[7];
cx q[5], q[3];
cx q[9], q[1];
cx q[14], q[0];
cx q[27], q[24];
cx q[19], q[15];
cx q[22], q[14];
cx q[9], q[7];
cx q[12], q[3];
cx q[5], q[1];
cx q[8], q[0];
cx q[30], q[27];
cx q[25], q[24];
cx q[21], q[19];
cx q[18], q[15];
cx q[16], q[14];
cx q[28], q[12];
cx q[8], q[7];
cx q[11], q[3];
cx q[2], q[1];
cx q[6], q[0];
cx q[13], q[5];
cx q[26], q[22];
cx q[29], q[27];
cx q[23], q[18];
cx q[20], q[16];
cx q[17], q[15];
cx q[19], q[12];
cx q[11], q[7];
cx q[10], q[6];
cx q[4], q[3];
cx q[2], q[0];
cx q[21], q[5];
cx q[24], q[8];
cx q[25], q[9];
cx q[14], q[13];
cx q[16], q[15];
cx q[23], q[7];
cx q[17], q[1];
cx q[4], q[0];
cx q[20], q[19];
cx q[6], q[5];
cx q[18], q[2];
cx q[27], q[11];
cx q[10], q[9];
cx q[12], q[8];
cx q[26], q[25];
cx q[22], q[21];
cx q[29], q[13];
cx q[28], q[24];
cx q[30], q[14];
