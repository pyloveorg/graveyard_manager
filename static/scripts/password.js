function password_strenght()
{
	var points= 0;
	var list = new Array();
	var password = document.getElementById("password").value;

	function next(a, b)
	{
		var tablica = [];
		var i = 0;
		for (n = a; n < b + 1; n ++)
		{
			tablica[i] = n;
			i += 1;
		}
		return tablica;
	}

	var classes =
	[
		next(33, 47).concat(next(58, 64), next(91, 96), next(123, 126)),
		next(48, 57),
		next(65, 90),
		next(97, 122)
	]

	if (password.length > 7)
		points += 1;

	for (i = 0; i < password.length; i ++)
		list[i] = password.charCodeAt(i);

	function verification(what, where)
	{
		var decision = false;

		for (i = 0; i < what.length; i ++)
		{
			decision = where.some(function (element) {
			return element === what[i]});

			if (decision == true)
				break;
		}
		return decision;
	}

	var answer = verification(classes[0], list);
		if (answer == true)
			points += 1;

	var answer = verification(classes[1], list);
		if (answer == true)
			points += 1;

	var answer = verification(classes[2], list);
		if (answer == true)
			points += 1;

	var answer = verification(classes[3], list);
		if (answer == true)
			points += 1;

	var contents_div = "";

	for (i = 1; i < points + 1; i ++)
		contents_div = contents_div + '<div class="password_square password_square--green">' +'</div>';

	for (i = 1; i < 6 - points; i ++)
		contents_div = contents_div + '<div class="password_square password_square--red">' +'</div>';

	document.getElementById("board").innerHTML = contents_div;

}

var changePw = document.getElementById('password')
changePw.addEventListener('input', password_strenght)
window.addEventListener('load', password_strenght)
