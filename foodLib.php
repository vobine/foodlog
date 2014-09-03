<?php

function newSQL ($user, $pwd)
{
  return new PDO ('mysql:host=localhost;dbname=food', $user, $pwd);
}

function querySQL ($pdo, $sql, $parameters)
{
  $stmt = $pdo->prepare ($sql);
  if ($stmt && $stmt->execute ($parameters)) {
    // Success!
  } else {
    // Boom!
    
  }
}
?>
