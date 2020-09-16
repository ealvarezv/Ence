function publish()
{
  var d = new Date();
  var utc = d.getTime() + (d.getTimezoneOffset() * 60000);  //This converts to UTC 00:00
  var time = new Date(utc + (3600000*2));
  var milliseconds = d.getMilliseconds();
  // var vars = time.split(" ");
  var message = time + "." + milliseconds;
  // var message = "hola";
  var Thread = Java.type("java.lang.Thread");
  // mqttspy.publish("/e2a5ec7650289479/alarm", "{\"type\":\"CLOSENESS_DANGER\",\"level\":\"HIGH\"}", 1, false);
  mqttspy.publish("/e2a5ec7650289479/alarm", "Timestamp: " +  message, 1, false);
  Thread.sleep(2000);
}
publish();
