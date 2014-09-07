<?php

/****************************************************************
 * Application configuration.
 *
 * Configuration file path is local, so we can find it.
 * Configuration file proper is not local, to hide it from HTTP.
 */

$confFile = "/etc/foodLog.conf";
try {
  $conf = fopen ($confFile, "rt");
} catch (Exception $e) {
  myBad ("Need a configuration file.");
}
while (! feof ($conf)) {
  $line = explode ("\t", trim (fgets ($conf), "\r\n\0"), 2);
  $CONF[$line[0]] = $line[1];
}
fclose ($conf);

/****************************************************************
 * SQL database adapter
 */

// Initiate a connection
function newSQL ($user, $pwd)
{
  return new PDO ('mysql:host=localhost;dbname=food', $user, $pwd);
}

// Execute a query, return cursor
function querySQL ($pdo, $sql, $parameters = array())
{
  $stmt = $pdo->prepare ($sql);
  if (! $stmt) {
    // SQL or connection failure?
    myBad ('Possible SQL error in: ' . $sql);
  } elseif (! $stmt->execute ($parameters)) {
    // Server, maybe?
    myBad ('Possible SQL server error on ' . $sql);
  }

  // Success!
  return $stmt;
}

?>
