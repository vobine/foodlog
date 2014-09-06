<?php

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
  } elseif ($! stmt->execute ($parameters)) {
    // Server, maybe?
    myBad ('Possible SQL server error on ' . $sql);
  }

  // Success!
  return $stmt;
}

?>
