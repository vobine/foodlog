<?php

function newSQL ($user, $pwd)
{
  return new PDO ('mysql:host=localhost;dbname=food', $user, $pwd);
}

function querySQL ($pdo, $sql, $parameters)
{
  $stmt = $pdo->prepare ($sql);
  if (!$stmt) {
    // SQL or connection failure?
    myBad ('Possible SQL error in: ' . $sql);
  } elseif ($stmt->execute ($parameters)) {
    // Server, maybe?
    myBad ('Possible SQL server error on ' . $sql);
  }

  // Success!
  return $stmt;
}

?>
