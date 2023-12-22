function stopAll() {
    var btns = document.querySelectorAll('button');
    btns.forEach(element => {
        element.disabled = true
    });
}

function copyText(txt) {
    try {
        navigator.clipboard.writeText(txt)
        var icon = document.querySelector(`#${txt} .cls .fa`),
            icon2 = document.getElementById('done')
        if (icon2) {
            icon2.className = 'fa fa-copy'
            icon2.id = ''
        }
        icon.className = 'fa fa-check'
        icon.id = 'done'
    } catch {
        alert("error durind copying the text")
    }
}

function unStopAll() {
    var btns = document.querySelectorAll('button');
    btns.forEach(element => {
        element.disabled = false
    });
}
function fetch(id) {
    return document.getElementById(id)
}
function hide(id, elm) {
    var toHide = fetch(id)
    toHide.style.display = 'none'
    elm.onclick = function () {
        show(id, elm)
    }
    elm.className = 'fa fa-align-right'
}
function show(id, elm) {
    var toShow = fetch(id)
    toShow.style.display = 'grid'
    elm.onclick = function () {
        hide(id, elm)
    }
    elm.className = 'fa fa-remove'
    let N = fetch('content')
    N.onclick = function () {
        hide(id, elm)
    }
}
function show2(elm) {
    try {
        var toShow = fetch('form')
        toShow.reset()
    } catch {
        var toShow = fetch('form_class')
        toShow.reset()
    }
    toShow.style.display = 'grid'
    elm.style.display = 'none'
}
function hide2(id, elm) {
    try {
        var toHide = fetch('form')
        toHide.reset()
    } catch {
        var toHide = fetch('form_class')
        toHide.reset()
    }
    toHide.style.display = 'none'
    elm.style.display = ''
}
function handleError(errorMessage, form) {
    var existingError = fetch('error-p');
    if (existingError) {
        form.removeChild(existingError);
    }

    var error = document.createElement('p');
    error.id = 'error-p';
    error.innerText = errorMessage;
    form.appendChild(error);
}
function submitNewGrade(form) {
    var req = new XMLHttpRequest(), formdata = new FormData(form),
        link = fetch('url_new_g').href
    req.open('POST', link)

    req.onreadystatechange = function () {
        if (req.readyState == 4 && req.status == 200) {
            try {
                var json = JSON.parse(req.responseText);
                if (json.exist == 1) {
                    handleError(json.error, form)
                    unStopAll()
                } else {
                    form.submit()
                }
            } catch {
                handleError('Internal Server Error', form)
                unStopAll()
            }
        }
    }
    req.send(formdata)
}
try {
    var g_form = document.getElementById('form')
    g_form.addEventListener('submit', function (ev) {
        stopAll()
        ev.preventDefault()
        submitNewGrade(this)
    })

} catch {
    var g_form = document.getElementById('form_class')
    g_form.addEventListener('submit', function (ev) {
        stopAll()
        ev.preventDefault()
        submitNewGrade(this)
    })

}