function show(id1, id2, id3, id4){
	if (document.getElementById(id1).style.display == "block" ||
		document.getElementById(id2).style.display == "block" ||
		document.getElementById(id3).style.display == "block"
		){
		document.getElementById(id1).style.display = "none";
		document.getElementById(id2).style.display = "none";
		document.getElementById(id3).style.display = "none";
	}
	document.getElementById(id4).style.display = "block";
}
