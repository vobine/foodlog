<!DOCTYPE html>

<html>
<head>

  <title>UI Mockup For Food Log</title>
  <link rel="stylesheet" type="text/css" href="foodlog.css" >

</head>

<body>

  <h1>UI Mockup for Food Log</h1>

<?php
require_once ('foodLib.php');

$sql = newSQL ($CONF["USER"], $CONF["PWD"]);
?>

  <div class="group" id="recent" >
    <ul>
<?php
$lately = querySQL ($sql, "SELECT fl.stamp, ft.fullName, fl.btype
FROM foodLog AS fl
LEFT JOIN foodType AS ft
ON fl.atype = ft.id
WHERE fl.stamp > DATE_SUB(CURDATE(), INTERVAL 7 DAY)
ORDER BY fl.stamp DESC");

$counter = 0;
foreach ($lately->fetch (PDO::FETCH_ASSOC) as $row) {
  printf ("<ul> %s %s %s </ul>\n",
          $row["fl.stamp"],
          $row["ft.fullName"],
          $row["fl.btype"]);
}
?>
    </ul>
  </div>

  <form method="post" action="enter.php" >

  <div class="group" id="summary" >
    <input type="submit" class="selector"
	   id="MF" value="MF"
	   title="Medifast meal" />
    <input type="submit" class="selector"
	   id="H2O" value="H2O" title="Water" />
    <input type="submit" class="selector"
	   id="Sup" value="Sup" title="Medifast supplement(s)" />
    <input type="submit" class="selector"
	   id="Lean" value="Lean" title="Lean protein" />
    <input type="submit" class="selector"
	   id="Grn" value="Grn" title="Green vegetables" />
    <input type="submit" class="selector"
	   id="Ex" value="Ex" title="Exercise" />
    <input type="submit" class="selector"
	   id="Off" value="Off" title="Off-plan food or other stuff" />
  </div>

  <div class="group" id="entry" >
    <label class="label" id="quaLabel" for="quaEntry" >Quantity:</label>
    <input type="number" class="entry" id="quaEntry" size="2" />
    <label class="label" id="noteLabel" for="noteEntry" >Note:</label>
    <input type="text" class="entry" id="noteEntry" />
  </div>
  </form>

  <div class="group" id="report" >
    <svg width="300px" height="300px"
	 viewbox="0 0 100 100" >
      <rect x="0" y="0" width="100" height="100"
	    fill="yellow" stroke="blue" strokewidth="12" />
      <polyline points="0,100 10,90 20,95 30,88 40,84 50,87 60,81"
		style="fill:none;stroke:black;stroke-width:1px" />
      What the hell browser are you trying to use?
      FFS, find one with SVG, and preferably from the 21st century!
    </svg>
    <table>
      <tr>
	<th>Date</th>
	<th>Medifast</th>
	<th>Water</th>
	<th>Supplements</th>
	<th>Lean</th>
	<th>Green</th>
	<th>Exercise</th>
	<th>Off plan</th>
      </tr>
      <tr>
	<td>8/31/2014</td>
	<td>5</td>
	<td>112</td>
	<td>3</td>
	<td>1</td>
	<td>1</td>
	<td>1</td>
	<td>0</td>
      </tr>
      <tr>
	<td>8/30/2014</td>
	<td>5</td>
	<td>120</td>
	<td>3</td>
	<td>1</td>
	<td>1</td>
	<td>1</td>
	<td>0</td>
      </tr>
    </table>
  </div>

</body>
</html>
