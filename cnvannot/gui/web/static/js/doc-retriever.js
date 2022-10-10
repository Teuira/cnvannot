function retrievePublicationsByGene(gene, onRetrieved, retry = 0) {
    let curr_retry = retry;
    let x = setInterval(function () {
        let httpRequest = new XMLHttpRequest();
        httpRequest.timeout = 120000;
        httpRequest.responseType = 'text';
        let str_query = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=' + gene + '&retmax=10000000';

        httpRequest.open('GET', str_query, true);
        httpRequest.onreadystatechange = function () {
            let parser;
            let xmlDoc;
            if (httpRequest.readyState === XMLHttpRequest.DONE) {
                let status = httpRequest.status;
                if (status === 0 || (status >= 200 && status < 400)) {
                    // OK.
                    parser = new DOMParser();
                    xmlDoc = parser.parseFromString(httpRequest.response, "text/xml");
                    onRetrieved(xmlDoc);
                } else {
                    // RETRY OR ERROR.
                    if (curr_retry === 5) {
                        alert("Sorry, Something went wrong!");
                        onRetrieved(null);
                        return;
                    }
                    console.log("Retry..");
                    retrievePublicationsByGene(gene, onRetrieved, ++curr_retry);
                }
            }
        };
        httpRequest.send();

        clearInterval(x);
    }, Math.floor(Math.random() * (2000 - 500 + 1) + 500));
}

function getPublicationIds(xmlDoc) {
    let res = [];

    let ids = xmlDoc.getElementsByTagName("IdList")[0].childNodes
    for (let i = 0; i < ids.length; i++) {
        if (ids[i].nodeName === 'Id')
            res.push(ids[i].innerHTML);
    }

    return res;
}

function retrieveAbstractsFromIds(ids, onRetrieved, retry = 0) {
    let curr_retry = retry;

    let idList = "";
    for (let i = 0; i < ids.length; i++) {
        idList += ids[i];
        if (i < ids.length - 1) {
            idList += ',';
        }
    }

    let x = setInterval(function () {
        let httpRequest = new XMLHttpRequest();
        httpRequest.timeout = 120000;
        httpRequest.responseType = 'text';
        let str_query = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=' + idList + '&retmode=XML&rettype=abstract';

        httpRequest.open('GET', str_query, true);
        httpRequest.onreadystatechange = function () {
            let parser;
            let xmlDoc;
            if (httpRequest.readyState === XMLHttpRequest.DONE) {
                let status = httpRequest.status;
                if (status === 0 || (status >= 200 && status < 400)) {
                    // OK.
                    parser = new DOMParser();
                    xmlDoc = parser.parseFromString(httpRequest.response, "text/xml");
                    console.log(xmlDoc);
                    onRetrieved(xmlDoc);
                } else {
                    // RETRY OR ERROR.
                    if (curr_retry === 5) {
                        alert("Sorry, Something went wrong!");
                        onRetrieved(null);
                        return;
                    }
                    console.log("Retry..");
                    retrieveAbstractsFromIds(ids, onRetrieved, ++curr_retry);
                }
            }
        };
        httpRequest.send();

        clearInterval(x);
    }, Math.floor(Math.random() * (1000 - 500 + 1) + 500));
}

function retrieve10AbstractsFromIds(ids, onRetrieved, offset = 0) {
    retrieveAbstractsFromIds(ids.slice(10 * offset, 10 * offset + 10), function (xmlDoc) {
        onRetrieved(xmlDoc.getElementsByTagName("PubmedArticleSet")[0].childNodes);
    })
}