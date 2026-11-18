OPENQASM 2.0;
include "qelib1.inc";

qreg q[53];
creg rec[38];

h q[1];
h q[3];
h q[0];
h q[4];
h q[11];
h q[10];
h q[7];
h q[8];
h q[2];
h q[5];
h q[21];
h q[13];
h q[6];
h q[26];
h q[17];
cx q[17], q[19];
cx q[26], q[24];
cx q[7], q[9];
h q[31];
cx q[31], q[29];
cx q[10], q[20];
cx q[6], q[14];
h q[32];
cx q[32], q[25];
cx q[1], q[23];
h q[33];
cx q[33], q[34];
h q[35];
cx q[35], q[36];
h q[37];
cx q[37], q[38];
h q[39];
cx q[39], q[40];
h q[41];
cx q[41], q[42];
cx q[26], q[29];
cx q[7], q[19];
cx q[10], q[18];
cx q[4], q[9];
cx q[1], q[25];
h q[43];
cx q[43], q[38];
h q[44];
cx q[44], q[39];
cx q[40], q[45];
cx q[17], q[20];
cx q[26], q[28];
cx q[7], q[14];
cx q[0], q[19];
cx q[10], q[15];
cx q[13], q[29];
cx q[4], q[30];
h q[46];
cx q[46], q[1];
cx q[9], q[23];
cx q[39], q[38];
cx q[28], q[27];
cx q[7], q[10];
cx q[0], q[15];
cx q[4], q[16];
cx q[11], q[29];
cx q[5], q[14];
cx q[38], q[40];
cx q[19], q[18];
cx q[27], q[47];
cx q[7], q[48];
h q[49];
cx q[49], q[0];
cx q[21], q[29];
cx q[4], q[12];
cx q[2], q[14];
cx q[28], q[1];
h q[50];
cx q[50], q[38];
cx q[11], q[16];
cx q[5], q[27];
cx q[7], q[51];
cx q[34], q[0];
cx q[4], q[22];
cx q[2], q[26];
cx q[3], q[12];
cx q[35], q[21];
cx q[49], q[52];
cx q[36], q[1];
cx q[24], q[47];
cx q[41], q[11];
measure q[47] -> rec[0];
cx q[8], q[7];
cx q[34], q[5];
cx q[35], q[26];
cx q[22], q[48];
cx q[3], q[29];
cx q[49], q[25];
cx q[15], q[51];
reset q[47];
cx q[28], q[47];
cx q[34], q[7];
cx q[6], q[28];
cx q[35], q[27];
cx q[9], q[48];
cx q[8], q[1];
cx q[42], q[3];
cx q[24], q[47];
cx q[20], q[51];
cx q[21], q[22];
cx q[49], q[18];
cx q[31], q[29];
measure q[47] -> rec[1];
measure q[48] -> rec[2];
h q[31]; measure q[31] -> rec[3]; h q[31]; // decomposed MX
cx q[34], q[25];
cx q[36], q[6];
cx q[4], q[8];
cx q[1], q[9];
cx q[42], q[7];
cx q[14], q[24];
cx q[49], q[20];
cx q[29], q[30];
cx q[19], q[51];
measure q[51] -> rec[4];
cx q[34], q[27];
cx q[52], q[8];
cx q[33], q[1];
reset q[31]; h q[31]; // decomposed RX
cx q[31], q[7];
reset q[47];
cx q[6], q[47];
cx q[13], q[4];
cx q[42], q[21];
cx q[35], q[14];
cx q[49], q[9];
reset q[48];
cx q[27], q[48];
cx q[46], q[1];
cx q[31], q[8];
cx q[50], q[47];
reset q[51];
cx q[4], q[51];
cx q[42], q[25];
cx q[52], q[14];
cx q[34], q[18];
cx q[41], q[13];
cx q[35], q[36];
cx q[7], q[38];
h q[35]; measure q[35] -> rec[5]; h q[35]; // decomposed MX
measure q[36] -> rec[6];
measure q[38] -> rec[7];
cx q[37], q[48];
cx q[31], q[1];
reset q[35]; h q[35]; // decomposed RX
cx q[35], q[51];
cx q[46], q[9];
cx q[42], q[30];
cx q[49], q[52];
cx q[34], q[20];
cx q[32], q[25];
measure q[52] -> rec[8];
h q[46]; measure q[46] -> rec[9]; h q[46]; // decomposed MX
h q[32]; measure q[32] -> rec[10]; h q[32]; // decomposed MX
cx q[48], q[47];
reset q[32];
cx q[1], q[32];
cx q[37], q[51];
cx q[42], q[9];
cx q[49], q[24];
cx q[33], q[34];
h q[49]; measure q[49] -> rec[11]; h q[49]; // decomposed MX
h q[33]; measure q[33] -> rec[12]; h q[33]; // decomposed MX
measure q[34] -> rec[13];
reset q[33]; h q[33]; // decomposed RX
cx q[33], q[47];
cx q[43], q[32];
reset q[34]; h q[34]; // decomposed RX
cx q[34], q[51];
cx q[5], q[48];
cx q[31], q[9];
cx q[41], q[42];
h q[41]; measure q[41] -> rec[14]; h q[41]; // decomposed MX
measure q[42] -> rec[15];
h q[31]; measure q[31] -> rec[16]; h q[31]; // decomposed MX
reset q[31]; h q[31]; // decomposed RX
cx q[31], q[47];
cx q[32], q[45];
cx q[51], q[39];
reset q[36]; h q[36]; // decomposed RX
cx q[36], q[34];
cx q[47], q[44];
cx q[50], q[32];
cx q[48], q[51];
reset q[38]; h q[38]; // decomposed RX
cx q[38], q[34];
cx q[31], q[37];
cx q[45], q[43];
cx q[22], q[36];
measure q[36] -> rec[17];
reset q[36]; h q[36]; // decomposed RX
cx q[36], q[47];
cx q[44], q[33];
cx q[23], q[32];
cx q[48], q[37];
cx q[38], q[35];
cx q[25], q[45];
cx q[12], q[34];
cx q[24], q[31];
h q[38]; measure q[38] -> rec[18]; h q[38]; // decomposed MX
measure q[45] -> rec[19];
measure q[34] -> rec[20];
measure q[31] -> rec[21];
reset q[31]; h q[31]; // decomposed RX
cx q[31], q[36];
cx q[32], q[51];
cx q[48], q[47];
cx q[26], q[33];
cx q[14], q[37];
h q[48]; measure q[48] -> rec[22]; h q[48]; // decomposed MX
measure q[33] -> rec[23];
measure q[37] -> rec[24];
cx q[31], q[44];
reset q[33]; h q[33]; // decomposed RX
cx q[33], q[36];
cx q[11], q[51];
cx q[32], q[40];
h q[31]; measure q[31] -> rec[25]; h q[31]; // decomposed MX
cx q[50], q[44];
reset q[31]; h q[31]; // decomposed RX
cx q[31], q[36];
cx q[51], q[39];
cx q[32], q[35];
cx q[33], q[47];
cx q[8], q[40];
h q[33]; measure q[33] -> rec[26]; h q[33]; // decomposed MX
measure q[40] -> rec[27];
cx q[50], q[43];
cx q[31], q[44];
cx q[51], q[35];
cx q[15], q[36];
cx q[20], q[47];
cx q[16], q[39];
h q[50]; measure q[50] -> rec[28]; h q[50]; // decomposed MX
h q[31]; measure q[31] -> rec[29]; h q[31]; // decomposed MX
h q[51]; measure q[51] -> rec[30]; h q[51]; // decomposed MX
measure q[36] -> rec[31];
measure q[47] -> rec[32];
measure q[39] -> rec[33];
cx q[32], q[43];
cx q[30], q[35];
cx q[19], q[44];
h q[32]; measure q[32] -> rec[34]; h q[32]; // decomposed MX
measure q[35] -> rec[35];
measure q[44] -> rec[36];
cx q[9], q[43];
measure q[43] -> rec[37];
