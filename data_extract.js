const net = require("net");
const client = net.createConnection(25025, "192.168.24.8", () => {
  // 'connect' listener.
  console.log("connected to server!");
  //   client.write("$PEKIO,GET_ANCHORS");
});
client.on("data", (data) => {
  console.log(data.toString());
  client.end();
});
// client.on("end", () => {
//   console.log("disconnected from server");
// });
client.on("error", (error) => {
  console.log("error from server", error);
});
client.on("ready", (ready) => {
  console.log("ready from server", ready);
  //client.write("$PEKIO,GET_ANCHORS\r\n");
  //client.write("$PEKIO,SET_REPORT_LIST,COORD\r\n");
  client.write("$PEKIO,GET_TAGS\r\n");
  
  //client.write("$PEKIO,COORD,Sequence Number, Tag's Serial Number, Tag's Position, Information String, Calculation's Timestamp\r\n")
  //client.write("$PEKIO,ADD_CUSTOM_REPORT_TYPE,COORD_DATA,OFF,SEQ_NR,0x001A2C,X,Y,Z,INFO_STR,ARRIVAL_TIME\r\n");
  //client.write("$PEKIO,SET_REPORT_LIST,,RR_L,COORD_E");

  
  // client.write("$PEKIO,ANCHOR_COORD\r\n");
  // client.write("$PEKIO,COORD\r\n");

  // 0x001A2C - Asset Tag
  // 0x001A79 - People Tag

  // In PuTTy, $PEKIO,SET_REPORT_LIST,COORD

  /*
  1) Two tags coming in from opposite directions
  2) One standing still inside a danger zone and the other entering danger zone towards it
  3) Two moving around a lot but not coming into close proximity
  
  */
});