OPENQASM 2.0;
include "qelib1.inc";

qreg q[157];

h q[8];
h q[19];
h q[3];
h q[32];
h q[2];
h q[48];
h q[1];
h q[42];
h q[0];
h q[18];
h q[31];
h q[47];
h q[74];
h q[12];
h q[11];
h q[10];
h q[9];
h q[29];
h q[45];
h q[72];
h q[63];
h q[23];
h q[22];
h q[21];
h q[20];
h q[43];
h q[70];
h q[61];
h q[56];
h q[36];
h q[35];
h q[34];
h q[33];
h q[68];
h q[59];
h q[54];
h q[51];
h q[65];
h q[57];
h q[53];
h q[49];
h q[85];
h q[103];
h q[121];
h q[139];
h q[102];
h q[120];
h q[138];
h q[156];
h q[87];
h q[89];
h q[91];
h q[93];
h q[94];
h q[96];
h q[98];
h q[100];
h q[105];
h q[107];
h q[109];
h q[111];
h q[112];
h q[114];
h q[116];
h q[118];
h q[123];
h q[125];
h q[127];
h q[129];
h q[130];
h q[132];
h q[134];
h q[136];
h q[141];
h q[143];
h q[145];
h q[147];
h q[148];
h q[150];
h q[152];
h q[154];
barrier q;

cx q[85], q[7];
cx q[87], q[6];
cx q[89], q[5];
cx q[91], q[4];
cx q[93], q[67];
barrier q;

cx q[8], q[85];
cx q[3], q[87];
cx q[2], q[89];
cx q[1], q[91];
cx q[0], q[93];
barrier q;

cx q[19], q[87];
cx q[32], q[89];
cx q[48], q[91];
cx q[42], q[93];
barrier q;

cx q[18], q[87];
cx q[31], q[89];
cx q[47], q[91];
cx q[74], q[93];
barrier q;

cx q[85], q[7];
cx q[87], q[6];
cx q[89], q[5];
cx q[91], q[4];
cx q[93], q[67];
barrier q;

cx q[102], q[66];
cx q[100], q[73];
cx q[98], q[46];
cx q[96], q[30];
cx q[94], q[16];
barrier q;

cx q[67], q[102];
cx q[4], q[100];
cx q[5], q[98];
cx q[6], q[96];
cx q[7], q[94];
barrier q;

cx q[74], q[100];
cx q[47], q[98];
cx q[31], q[96];
cx q[18], q[94];
barrier q;

cx q[9], q[100];
cx q[10], q[98];
cx q[11], q[96];
cx q[12], q[94];
barrier q;

cx q[102], q[66];
cx q[100], q[73];
cx q[98], q[46];
cx q[96], q[30];
cx q[94], q[16];
barrier q;

cx q[103], q[17];
cx q[105], q[15];
cx q[107], q[14];
cx q[109], q[13];
cx q[111], q[76];
barrier q;

cx q[16], q[103];
cx q[30], q[105];
cx q[46], q[107];
cx q[73], q[109];
cx q[66], q[111];
barrier q;

cx q[12], q[105];
cx q[11], q[107];
cx q[10], q[109];
cx q[9], q[111];
barrier q;

cx q[29], q[105];
cx q[45], q[107];
cx q[72], q[109];
cx q[63], q[111];
barrier q;

cx q[103], q[17];
cx q[105], q[15];
cx q[107], q[14];
cx q[109], q[13];
cx q[111], q[76];
barrier q;

cx q[120], q[75];
cx q[118], q[62];
cx q[116], q[71];
cx q[114], q[44];
cx q[112], q[28];
barrier q;

cx q[76], q[120];
cx q[13], q[118];
cx q[14], q[116];
cx q[15], q[114];
cx q[17], q[112];
barrier q;

cx q[63], q[118];
cx q[72], q[116];
cx q[45], q[114];
cx q[29], q[112];
barrier q;

cx q[20], q[118];
cx q[21], q[116];
cx q[22], q[114];
cx q[23], q[112];
barrier q;

cx q[120], q[75];
cx q[118], q[62];
cx q[116], q[71];
cx q[114], q[44];
cx q[112], q[28];
barrier q;

cx q[121], q[27];
cx q[123], q[26];
cx q[125], q[25];
cx q[127], q[24];
cx q[129], q[78];
barrier q;

cx q[28], q[121];
cx q[44], q[123];
cx q[71], q[125];
cx q[62], q[127];
cx q[75], q[129];
barrier q;

cx q[23], q[123];
cx q[22], q[125];
cx q[21], q[127];
cx q[20], q[129];
barrier q;

cx q[43], q[123];
cx q[70], q[125];
cx q[61], q[127];
cx q[56], q[129];
barrier q;

cx q[121], q[27];
cx q[123], q[26];
cx q[125], q[25];
cx q[127], q[24];
cx q[129], q[78];
barrier q;

cx q[138], q[77];
cx q[136], q[55];
cx q[134], q[60];
cx q[132], q[69];
cx q[130], q[40];
barrier q;

cx q[78], q[138];
cx q[24], q[136];
cx q[25], q[134];
cx q[26], q[132];
cx q[27], q[130];
barrier q;

cx q[56], q[136];
cx q[61], q[134];
cx q[70], q[132];
cx q[43], q[130];
barrier q;

cx q[33], q[136];
cx q[34], q[134];
cx q[35], q[132];
cx q[36], q[130];
barrier q;

cx q[138], q[77];
cx q[136], q[55];
cx q[134], q[60];
cx q[132], q[69];
cx q[130], q[40];
barrier q;

cx q[139], q[41];
cx q[141], q[39];
cx q[143], q[38];
cx q[145], q[37];
cx q[147], q[79];
barrier q;

cx q[40], q[139];
cx q[69], q[141];
cx q[60], q[143];
cx q[55], q[145];
cx q[77], q[147];
barrier q;

cx q[36], q[141];
cx q[35], q[143];
cx q[34], q[145];
cx q[33], q[147];
barrier q;

cx q[68], q[141];
cx q[59], q[143];
cx q[54], q[145];
cx q[51], q[147];
barrier q;

cx q[139], q[41];
cx q[141], q[39];
cx q[143], q[38];
cx q[145], q[37];
cx q[147], q[79];
barrier q;

cx q[156], q[80];
cx q[154], q[50];
cx q[152], q[52];
cx q[150], q[58];
cx q[148], q[64];
barrier q;

cx q[79], q[156];
cx q[37], q[154];
cx q[38], q[152];
cx q[39], q[150];
cx q[41], q[148];
barrier q;

cx q[51], q[154];
cx q[54], q[152];
cx q[59], q[150];
cx q[68], q[148];
barrier q;

cx q[49], q[154];
cx q[53], q[152];
cx q[57], q[150];
cx q[65], q[148];
barrier q;

cx q[156], q[80];
cx q[154], q[50];
cx q[152], q[52];
cx q[150], q[58];
cx q[148], q[64];
barrier q;

