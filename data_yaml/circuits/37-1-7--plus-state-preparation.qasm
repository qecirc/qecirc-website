OPENQASM 2.0;
include "qelib1.inc";

qreg q[37];

reset q[31];
reset q[23];
reset q[21];
reset q[18];
reset q[17];
reset q[12];
reset q[11];
reset q[10];
reset q[9];
reset q[7];
reset q[6];
reset q[5];
reset q[3];
reset q[2];
reset q[1];
reset q[29];
reset q[0];
reset q[19];
reset q[14]; h q[14]; // decomposed RX
reset q[4]; h q[4]; // decomposed RX
reset q[27]; h q[27]; // decomposed RX
reset q[33]; h q[33]; // decomposed RX
reset q[15]; h q[15]; // decomposed RX
reset q[8]; h q[8]; // decomposed RX
reset q[20]; h q[20]; // decomposed RX
reset q[35]; h q[35]; // decomposed RX
reset q[36]; h q[36]; // decomposed RX
reset q[24]; h q[24]; // decomposed RX
reset q[16]; h q[16]; // decomposed RX
reset q[34]; h q[34]; // decomposed RX
reset q[22]; h q[22]; // decomposed RX
reset q[28]; h q[28]; // decomposed RX
reset q[32]; h q[32]; // decomposed RX
reset q[13]; h q[13]; // decomposed RX
reset q[25]; h q[25]; // decomposed RX
reset q[30]; h q[30]; // decomposed RX
reset q[26]; h q[26]; // decomposed RX
cx q[30], q[19];
cx q[35], q[7];
cx q[26], q[0];
cx q[28], q[1];
cx q[34], q[5];
cx q[20], q[6];
cx q[4], q[11];
cx q[13], q[12];
cx q[25], q[17];
cx q[15], q[3];
cx q[16], q[9];
cx q[27], q[10];
cx q[22], q[21];
cx q[24], q[23];
cx q[36], q[7];
cx q[30], q[18];
cx q[35], q[31];
cx q[25], q[20];
cx q[34], q[0];
cx q[19], q[4];
cx q[12], q[5];
cx q[11], q[6];
cx q[13], q[28];
cx q[8], q[1];
cx q[15], q[16];
cx q[22], q[24];
cx q[17], q[36];
cx q[7], q[2];
cx q[14], q[18];
cx q[32], q[31];
cx q[33], q[35];
cx q[20], q[26];
cx q[5], q[3];
cx q[23], q[6];
cx q[11], q[10];
cx q[4], q[21];
cx q[34], q[32];
cx q[35], q[28];
cx q[2], q[29];
cx q[36], q[0];
cx q[33], q[27];
cx q[9], q[14];
cx q[18], q[31];
cx q[20], q[11];
cx q[21], q[23];
cx q[6], q[4];
cx q[10], q[25];
cx q[1], q[7];
cx q[26], q[30];
cx q[36], q[33];
cx q[28], q[29];
cx q[31], q[12];
cx q[14], q[5];
cx q[18], q[34];
cx q[32], q[13];
cx q[8], q[2];
cx q[27], q[17];
cx q[3], q[9];
cx q[0], q[19];
