<?php
require_once ('foodLib.php');

$sql = newSQL ($CONF["USER"], $CONF["PWD"]);

$insert = querySQL ($sql,
		    "INSERT INTO
weight (weight, note)
VALUES (?, ?)",
		    array ($_REQUEST["weightEntry"],
			   $_REQUEST["noteEntry"]));

if ($sql->errorCode () == 0) {
  // Insertion successful! No need to display the error cruft.
  header ("HTTP/1.1: 303 See Other");
  header ("Location: show.php");
  die ();
}
?>

<!DOCTYPE html>

<html>

<head>
  <title>Database Insertion error for Food Log</title>
</head>

<body>

<div>
<a href="show.php">More!</a> 
</div>

<pre>
<?php
var_dump ($sql->errorCode ());
var_dump ($sql->errorInfo ());
var_dump ($type);
var_dump ($insert);
var_dump ($_REQUEST);
?>
</pre>

</body>
</html>
