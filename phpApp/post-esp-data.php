<?php

/*
  Rui Santos
  Complete project details at https://RandomNerdTutorials.com/esp32-esp8266-mysql-database-php/
  
  Permission is hereby granted, free of charge, to any person obtaining a copy
  of this software and associated documentation files.
  
  The above copyright notice and this permission notice shall be included in all
  copies or substantial portions of the Software.
*/

$servername = "172.17.0.2";

// REPLACE with your Database name
$dbname = "dserp200";
// REPLACE with Database user
$username = "esp32";
// REPLACE with Database user password
$password = "!123Cambodia";
// Keep this API Key value to be compatible with the ESP32 code provided in the project page. 
// If you change this value, the ESP32 sketch needs to match
$api_key_value = "tPmAT5Ab3j7F9";

$row_off_limit =$row_on_limit = $row_switch=$api_key = $status = $solar_power  = $ac_power=$in_power =$battery ="";

if ($_SERVER["REQUEST_METHOD"] == "GET") {
    $api_key = ($_GET["api_key"]);
    if($api_key == $api_key_value) {

        $status = ($_GET["status"]);
        $solar_power = ($_GET["sp"]);
        $ac_power = ($_GET["ap"]);
        $in_power = ($_GET["ip"]);
        $battery = ($_GET["btty"]);
      

        // Create connection
        $conn = new mysqli($servername, $username, $password, $dbname);
        // Check connection
        if ($conn->connect_error) {
            die("Connection failed: " . $conn->connect_error);
        } 
        
        $sql = "INSERT INTO log (status, solar_power,ac_power,in_power,battery)VALUES ($status , $solar_power  , $ac_power,$in_power ,$battery )";
        
        if ($conn->query($sql) === TRUE) {
            $sql2 = "SELECT switch,on_limit,off_limit FROM controll";
            if ($result = $conn->query($sql2)) {
                while ($row = $result->fetch_assoc()) {
                    $row_switch = $row["switch"];
                    $row_on_limit = $row["on_limit"];
                    $row_off_limit = $row["off_limit"];
                echo "switch=$row_switch,on_limit=$row_on_limit,off_limit=$row_off_limit";
                }
                $result->free();
        } }
        else {
            echo "Error: " . $sql . "<br>" . $conn->error;
        }
        
        $conn->close();
    }
    else {
        echo "Wrong API Key provided.";
    }

}
else {
    echo "No data posted with HTTP POST.";
}

function test_input($data) {
    $data = trim($data);
    $data = stripslashes($data);
    $data = htmlspecialchars($data);
    return $data;
}
