/* Making XHR Request */
function makeRequestForProject(api_url, projectName) {
    // Check for various requests, to raise confirmation alert/prompt.
    let answer = null;

    if(api_url.search('delete') > -1){
        answer = confirm("Do you want to delete the project: "+ projectName);
    } else if(api_url.search('activ') > -1) {
        answer = confirm("Do you want to activate the project: "+ projectName);
    } else if(api_url.search('archive') > -1) {
        answer = confirm("Do you want to archive the project: "+ projectName);
    } else if(api_url.search('edit') > -1) {
        answer = confirm("Do you want to edit the project: "+ projectName);
    } else {
        console.log("Unknown request: " + api_url);
    }

    if (answer === true) {
        // Do the action here
        var params = 'project_name='+projectName;
        makeXMLHttpRequest("GET", api_url, params);
    } else if(answer === null) {
        // raise the toast, that request is unknown
        raiseToast('Unknown Request.');
    } else {
        // raise the toast, that action is cancelled
        raiseToast('Cancelled');
    }
}

function makeRequestForCrawler(url) {
    makeXMLHttpRequest("GET", url);
}

// ===============================
// Core method for XHR Request
// ===============================
function makeXMLHttpRequest(method, url, params, headers) {
    // If answer is true then proceed

        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
               // Typical action to be performed when the document is ready:
               raiseToast(xhttp.responseText);
               // refresh the page
               setTimeout(function(){
                    window.location.reload();
               }, 1000);
            }
            else if(this.readyState == 4 && this.status == 404) {
                // raise the toast now
                raiseToast('Sorry, 404; Not found');
            }
            else if(this.readyState == 4 && this.status == 500) {
                // raise the toast now
                raiseToast('Sorry, Error-500; Something went wrong at server side.');
            } else {
                // raise the toast now
                raiseToast('In Progress ...');
            }
        };

        if(method.search("GET") > -1) {
            if (params === undefined) {
                xhttp.open(method, url, true);
            } else {
                xhttp.open(method, url + "?" + params, true);
            }
        } else {
            xhttp.open(method, url, true);
        }

        xhttp.send();
}