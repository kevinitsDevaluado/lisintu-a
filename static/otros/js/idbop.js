// fetch('http://127.0.0.1:8000/getdata').then(function (response) {
// 	return response.json();
// }).then(function (jsondata) {
// 	console.log(jsondata);
// });

// var dbPromise = idb.open('feeds-db', 1, function (upgradeDb) {
// 	upgradeDb.createObjectStore('feeds', { keyPath: 'pk' });
// });


var dbPromise = idb.open('MTOP-db', 1, function (upgradeDb) {
	upgradeDb.createObjectStore('proyectos', { keyPath: 'pk' });
});


//collect latest post from server and store in idb
//https://mtop-pastaza.herokuapp.com/getdata/
//
fetch('http://127.0.0.1:8000/getdata').then(function (response) {
	return response.json();
}).then(function (jsondata) {
	dbPromise.then(function (db) {
		var tx = db.transaction('proyectos', 'readwrite');
		var feedsStore = tx.objectStore('proyectos');
		for (var key in jsondata) {
			if (jsondata.hasOwnProperty(key)) {
				feedsStore.put(jsondata[key]);
			}
		}
	});
});

//retrive data from idb and display on page
var post = "";
dbPromise.then(function (db) {
	var tx = db.transaction('proyectos', 'readonly');
	var feedsStore = tx.objectStore('proyectos');
	return feedsStore.openCursor();
}).then(function logItems(cursor) {
	if (!cursor) {
		document.getElementById('myTable').innerHTML = post;
		return;
	}
	for (var field in cursor.value) {
		if (field == 'fields') {
			feedsData = cursor.value[field];
			for (var key in feedsData) {
				if (key == 'codigo_man') {
					var title = '<td>' + feedsData[key] + '</td>';
				}
				if (key == 'estado_man') {
					var author = '<td>' + feedsData[key] + '</td>';
				}
				if (key == 'fecha_ingreso_man') {
					var body = '<td>' + feedsData[key] + '</td>';
				}
				if (key == 'tipo_man') {
					var estante = '<td>' + feedsData[key] + '</td>';
				}
				if (key == 'tipo_equipo_man') {
					var caja = '<td>' + feedsData[key] + '</td>';
				}
				if (key == 'costo_man') {
					var costo = '<td>' + feedsData[key] + '</td>';
				}
			}
			post = post + '<tr>' + title + '' + author + '' + body + '' + estante + '' + caja + '' + costo + '</tr>';
		}
	}
	return cursor.continue().then(logItems);
});



function getClientes()
{
	console.log(' *************** ');
	var request = window.indexedDB.open("MTOP-db");
	request.onsuccess = function(e) {
		var db =  e.target.result;
		var objectStore = db.transaction("proyectos").objectStore("proyectos");
		objectStore.openCursor().onsuccess = function(event) {
			var cursor = event.target.result;
			if (cursor) {
				console.log('ID -> ' + cursor.value.pk);
				console.log('NOMBRE -> ' + cursor.value.codigo_proyecto);
				console.log('EDAD -> ' + cursor.value.nombre_proyecto);
				console.log(' *************** ');
				cursor.continue();
			}
		}
	}
}