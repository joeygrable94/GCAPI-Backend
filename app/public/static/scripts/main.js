
function refreshIn(time) {
    setTimeout(function () {
        window.location.reload();
    }, time);
}

function geotagImageAndRerenderImage(e) {
    e.preventDefault();
    const values = Object.values(e.currentTarget).reduce((obj,field) => { obj[field.name] = field.value; return obj }, {});
    const value_string = Object.keys(values).reduce(function(a,k){a.push(k+'='+encodeURIComponent(values[k]));return a},[]).join('&');
    const tag_img_url = '/geotag/'+parseInt(values['image_id_val']);
    let x = new XMLHttpRequest();
    x.open( "POST", tag_img_url , true);
    x.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
    x.send(value_string);
    x.onload = function(e) {
        let resp = JSON.parse(this.responseText);
        console.log(resp);
    };
}

function geotagLookupLocationCoordinates(e) {
    e.preventDefault();
    const values = Object.values(e.currentTarget).reduce((obj,field) => { obj[field.name] = field.value; return obj }, {});
    const value_string = Object.keys(values).reduce(function(a,k){a.push(k+'='+encodeURIComponent(values[k]));return a},[]).join('&');
    const loc_lookup_url = '/geotag/location/coordinates';
    const show_lat = document.getElementById('ll_coord_latitude');
    const show_lon = document.getElementById('ll_coord_longitude');
    const show_addr = document.getElementById('ll_coord_address');
    console.log(show_addr);
    const show_error = document.getElementById('ll_coord_address_error');
    let x = new XMLHttpRequest();
    x.open( "POST", loc_lookup_url , true);
    x.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
    x.send(value_string);
    x.onload = function(e) {
        let resp = JSON.parse(this.responseText);
        if (resp.hasOwnProperty('error')) {
            if (ll_coord_address_error.classList.contains('hidden')) {
                ll_coord_address_error.classList.remove('hidden'); }
            show_error.innerHTML = resp.error;
            show_addr.innerHTML = '';
            show_lat.innerHTML = '';
            show_lon.innerHTML = '';
        }
        if (resp.hasOwnProperty('latitude') && resp.hasOwnProperty('longitude') && resp.hasOwnProperty('address')) {
            if (!ll_coord_address_error.classList.contains('hidden')) {
                ll_coord_address_error.classList.add('hidden'); }
            show_addr.innerHTML = resp.address;
            show_lat.innerHTML = resp.latitude + ', ';
            show_lon.innerHTML = resp.longitude;
        }
    };
}

function downloadImageAndRefresh(e) {
    const download_url = '/geotag/'+e.target.dataset.imageid+'/download';
    let x = new XMLHttpRequest();
    var headerMap = {};
    x.open( "POST", download_url , true);
    x.responseType = "blob";
    x.send();
    x.onload = function(e) {
        // Get the raw header string
        var headers = x.getAllResponseHeaders();
        // Convert the header string into an array of individual headers
        var arr = headers.trim().split(/[\r\n]+/);
        // Create a map of header names to values
        arr.forEach(function(line) {
            var parts = line.split(': ');
            var header = parts.shift();
            var value = parts.join(': ');
            headerMap[header] = value;
        });
        // Get the file name from the headers content-disposition
        const download_name = headerMap['content-disposition'].split('attachment; filename=')[1];
        return download(e.target.response, download_name, headerMap['content-type']);
    };
    // refreshIn(100);
}

function downloadAllImageUploadsAndRefresh(e) {
    const download_url = '/geotag/download/all';
    let x = new XMLHttpRequest();
    var headerMap = {};
    x.open( "POST", download_url , true);
    x.responseType = "blob";
    x.send();
    x.onload = function(e) {
        // Get the raw header string
        var headers = x.getAllResponseHeaders();
        // Convert the header string into an array of individual headers
        var arr = headers.trim().split(/[\r\n]+/);
        // Create a map of header names to values
        arr.forEach(function(line) {
            var parts = line.split(': ');
            var header = parts.shift();
            var value = parts.join(': ');
            headerMap[header] = value;
        });
        // Get the file name from the headers content-disposition
        const download_name = headerMap['content-disposition'].split('attachment; filename=')[1];
        return download(e.target.response, download_name, headerMap['content-type']);
    };
    // refreshIn(100);
}

function downloadOnlyTaggedImageUploadsAndRefresh(e) {
    const download_url = '/geotag/download/tagged';
    let x = new XMLHttpRequest();
    var headerMap = {};
    x.open( "POST", download_url , true);
    x.responseType = "blob";
    x.send();
    x.onload = function(e) {
        // Get the raw header string
        var headers = x.getAllResponseHeaders();
        // Convert the header string into an array of individual headers
        var arr = headers.trim().split(/[\r\n]+/);
        // Create a map of header names to values
        arr.forEach(function(line) {
            var parts = line.split(': ');
            var header = parts.shift();
            var value = parts.join(': ');
            headerMap[header] = value;
        });
        // Get the file name from the headers content-disposition
        const download_name = headerMap['content-disposition'].split('attachment; filename=')[1];
        return download(e.target.response, download_name, headerMap['content-type']);
    };
    // refreshIn(300);
}

// ---------------------------------------------------------------------------
// LOADER
if ( 'loading' === document.readyState ) {
    // The DOM has not yet been loaded.
    document.addEventListener( 'DOMContentLoaded', initGCAPI );
} else {
    // The DOM has already been loaded.
    initGCAPI();
}

// Initiate the menus when the DOM loads.
function initGCAPI() {
    // Download All Uploads
    const download_all_uploads = document.getElementById('geotag-action-download-all-uploads');
    download_all_uploads.addEventListener('click', downloadAllImageUploadsAndRefresh);
    // Download Only Tagged
    // const download_only_tagged = document.getElementById('geotag-action-download-only-tagged');
    // download_only_tagged.addEventListener('click', downloadOnlyTaggedImageUploadsAndRefresh);
    // Download Single Image
    let download_actions = document.getElementsByClassName('geotag-action-download');
    for (let i = download_actions.length - 1; i >= 0; i--) {
        download_actions[i].addEventListener('click', downloadImageAndRefresh);
    }
    // GeoTag Image
    let geotag_actions = document.getElementsByClassName('geotag-action-tag');
    for (var i = geotag_actions.length - 1; i >= 0; i--) {
        geotag_actions[i].addEventListener('submit', geotagImageAndRerenderImage);
    }
    // Lookup Image GeoTag
    const lookup_location_coords = document.getElementById('lookup-location-coordinates');
    lookup_location_coords.addEventListener('submit', geotagLookupLocationCoordinates);
}
