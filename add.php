<!DOCTYPE html>

<html>

<head>

  <title>Database Insertion for Food Log</title>
</head>

<?php
require_once ('foodLib.php');

$sql = newSQL ($CONF["USER"], $CONF["PWD"]);
var_dump ($sql);

$typeQuery = querySQL ($sql,
		       "SELECT *
FROM foodType
WHERE nickName = ?",
		       array ($_REQUEST["submit"]));
$type = $typeQuery->fetch (PDO::FETCH_ASSOC);

$insert = querySQL ($sql,
		    "INSERT INTO
foodLog (atype, quantity, comment)
VALUES (?, ?, ?)",
		    array ($type["id"],
			   $_REQUEST["quaEntry"],
			   $_REQUEST["noteEntry"]));
?>

<body>

<pre>
<?php
  var_dump ($type);
var_dump ($insert);
var_dump ($_REQUEST);
?>
</pre>

</body>
</html>
