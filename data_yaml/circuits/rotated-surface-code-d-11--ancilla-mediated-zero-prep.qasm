OPENQASM 2.0;
include "qelib1.inc";

qreg q[241];

h q[90];
h q[103];
h q[58];
h q[42];
h q[28];
h q[16];
h q[3];
h q[13];
h q[25];
h q[39];
h q[55];
h q[89];
h q[82];
h q[92];
h q[105];
h q[60];
h q[44];
h q[30];
h q[2];
h q[12];
h q[24];
h q[38];
h q[54];
h q[81];
h q[76];
h q[84];
h q[94];
h q[107];
h q[62];
h q[46];
h q[1];
h q[11];
h q[23];
h q[37];
h q[53];
h q[75];
h q[72];
h q[78];
h q[86];
h q[96];
h q[109];
h q[64];
h q[0];
h q[10];
h q[22];
h q[36];
h q[52];
h q[71];
h q[70];
h q[74];
h q[80];
h q[88];
h q[98];
h q[111];
h q[102];
h q[113];
h q[115];
h q[117];
h q[119];
h q[120];
cx q[90], q[127];
cx q[103], q[149];
cx q[58], q[171];
cx q[42], q[193];
cx q[28], q[215];
cx q[16], q[236];
barrier q;

cx q[127], q[100];
cx q[149], q[57];
cx q[171], q[41];
cx q[193], q[27];
cx q[215], q[15];
cx q[236], q[4];
barrier q;

cx q[127], q[99];
cx q[149], q[56];
cx q[171], q[40];
cx q[193], q[26];
cx q[215], q[14];
barrier q;

cx q[127], q[69];
cx q[149], q[51];
cx q[171], q[35];
cx q[193], q[21];
cx q[215], q[9];
barrier q;

cx q[90], q[127];
cx q[103], q[149];
cx q[58], q[171];
cx q[42], q[193];
cx q[28], q[215];
cx q[16], q[236];
barrier q;

cx q[3], q[226];
cx q[13], q[204];
cx q[25], q[182];
cx q[39], q[160];
cx q[55], q[138];
cx q[89], q[121];
barrier q;

cx q[226], q[16];
cx q[204], q[28];
cx q[182], q[42];
cx q[160], q[58];
cx q[138], q[103];
cx q[121], q[90];
barrier q;

cx q[226], q[9];
cx q[204], q[21];
cx q[182], q[35];
cx q[160], q[51];
cx q[138], q[69];
barrier q;

cx q[226], q[29];
cx q[204], q[43];
cx q[182], q[59];
cx q[160], q[104];
cx q[138], q[91];
barrier q;

cx q[3], q[226];
cx q[13], q[204];
cx q[25], q[182];
cx q[39], q[160];
cx q[55], q[138];
cx q[89], q[121];
barrier q;

cx q[82], q[129];
cx q[92], q[151];
cx q[105], q[173];
cx q[60], q[195];
cx q[44], q[217];
cx q[30], q[237];
barrier q;

cx q[129], q[89];
cx q[151], q[55];
cx q[173], q[39];
cx q[195], q[25];
cx q[217], q[13];
cx q[237], q[3];
barrier q;

cx q[129], q[91];
cx q[151], q[104];
cx q[173], q[59];
cx q[195], q[43];
cx q[217], q[29];
barrier q;

cx q[129], q[68];
cx q[151], q[50];
cx q[173], q[34];
cx q[195], q[20];
cx q[217], q[8];
barrier q;

cx q[82], q[129];
cx q[92], q[151];
cx q[105], q[173];
cx q[60], q[195];
cx q[44], q[217];
cx q[30], q[237];
barrier q;

cx q[2], q[228];
cx q[12], q[206];
cx q[24], q[184];
cx q[38], q[162];
cx q[54], q[140];
cx q[81], q[122];
barrier q;

cx q[228], q[30];
cx q[206], q[44];
cx q[184], q[60];
cx q[162], q[105];
cx q[140], q[92];
cx q[122], q[82];
barrier q;

cx q[228], q[8];
cx q[206], q[20];
cx q[184], q[34];
cx q[162], q[50];
cx q[140], q[68];
barrier q;

cx q[228], q[45];
cx q[206], q[61];
cx q[184], q[106];
cx q[162], q[93];
cx q[140], q[83];
barrier q;

cx q[2], q[228];
cx q[12], q[206];
cx q[24], q[184];
cx q[38], q[162];
cx q[54], q[140];
cx q[81], q[122];
barrier q;

cx q[76], q[131];
cx q[84], q[153];
cx q[94], q[175];
cx q[107], q[197];
cx q[62], q[219];
cx q[46], q[238];
barrier q;

cx q[131], q[81];
cx q[153], q[54];
cx q[175], q[38];
cx q[197], q[24];
cx q[219], q[12];
cx q[238], q[2];
barrier q;

cx q[131], q[83];
cx q[153], q[93];
cx q[175], q[106];
cx q[197], q[61];
cx q[219], q[45];
barrier q;

cx q[131], q[67];
cx q[153], q[49];
cx q[175], q[33];
cx q[197], q[19];
cx q[219], q[7];
barrier q;

cx q[76], q[131];
cx q[84], q[153];
cx q[94], q[175];
cx q[107], q[197];
cx q[62], q[219];
cx q[46], q[238];
barrier q;

cx q[1], q[230];
cx q[11], q[208];
cx q[23], q[186];
cx q[37], q[164];
cx q[53], q[142];
cx q[75], q[123];
barrier q;

cx q[230], q[46];
cx q[208], q[62];
cx q[186], q[107];
cx q[164], q[94];
cx q[142], q[84];
cx q[123], q[76];
barrier q;

cx q[230], q[7];
cx q[208], q[19];
cx q[186], q[33];
cx q[164], q[49];
cx q[142], q[67];
barrier q;

cx q[230], q[63];
cx q[208], q[108];
cx q[186], q[95];
cx q[164], q[85];
cx q[142], q[77];
barrier q;

cx q[1], q[230];
cx q[11], q[208];
cx q[23], q[186];
cx q[37], q[164];
cx q[53], q[142];
cx q[75], q[123];
barrier q;

cx q[72], q[133];
cx q[78], q[155];
cx q[86], q[177];
cx q[96], q[199];
cx q[109], q[221];
cx q[64], q[239];
barrier q;

cx q[133], q[75];
cx q[155], q[53];
cx q[177], q[37];
cx q[199], q[23];
cx q[221], q[11];
cx q[239], q[1];
barrier q;

cx q[133], q[77];
cx q[155], q[85];
cx q[177], q[95];
cx q[199], q[108];
cx q[221], q[63];
barrier q;

cx q[133], q[66];
cx q[155], q[48];
cx q[177], q[32];
cx q[199], q[18];
cx q[221], q[6];
barrier q;

cx q[72], q[133];
cx q[78], q[155];
cx q[86], q[177];
cx q[96], q[199];
cx q[109], q[221];
cx q[64], q[239];
barrier q;

cx q[0], q[232];
cx q[10], q[210];
cx q[22], q[188];
cx q[36], q[166];
cx q[52], q[144];
cx q[71], q[124];
barrier q;

cx q[232], q[64];
cx q[210], q[109];
cx q[188], q[96];
cx q[166], q[86];
cx q[144], q[78];
cx q[124], q[72];
barrier q;

cx q[232], q[6];
cx q[210], q[18];
cx q[188], q[32];
cx q[166], q[48];
cx q[144], q[66];
barrier q;

cx q[232], q[110];
cx q[210], q[97];
cx q[188], q[87];
cx q[166], q[79];
cx q[144], q[73];
barrier q;

cx q[0], q[232];
cx q[10], q[210];
cx q[22], q[188];
cx q[36], q[166];
cx q[52], q[144];
cx q[71], q[124];
barrier q;

cx q[70], q[135];
cx q[74], q[157];
cx q[80], q[179];
cx q[88], q[201];
cx q[98], q[223];
cx q[111], q[240];
barrier q;

cx q[135], q[71];
cx q[157], q[52];
cx q[179], q[36];
cx q[201], q[22];
cx q[223], q[10];
cx q[240], q[0];
barrier q;

cx q[135], q[73];
cx q[157], q[79];
cx q[179], q[87];
cx q[201], q[97];
cx q[223], q[110];
barrier q;

cx q[135], q[65];
cx q[157], q[47];
cx q[179], q[31];
cx q[201], q[17];
cx q[223], q[5];
barrier q;

cx q[70], q[135];
cx q[74], q[157];
cx q[80], q[179];
cx q[88], q[201];
cx q[98], q[223];
cx q[111], q[240];
barrier q;

cx q[102], q[234];
cx q[113], q[212];
cx q[115], q[190];
cx q[117], q[168];
cx q[119], q[146];
cx q[120], q[125];
barrier q;

cx q[234], q[111];
cx q[212], q[98];
cx q[190], q[88];
cx q[168], q[80];
cx q[146], q[74];
cx q[125], q[70];
barrier q;

cx q[234], q[5];
cx q[212], q[17];
cx q[190], q[31];
cx q[168], q[47];
cx q[146], q[65];
barrier q;

cx q[234], q[101];
cx q[212], q[112];
cx q[190], q[114];
cx q[168], q[116];
cx q[146], q[118];
barrier q;

cx q[102], q[234];
cx q[113], q[212];
cx q[115], q[190];
cx q[117], q[168];
cx q[119], q[146];
cx q[120], q[125];
barrier q;

