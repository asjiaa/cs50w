import { load_chart } from './util.js';

document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('#search-form').onsubmit = get_data;
    document.querySelectorAll('.fill-search').forEach(button => {
        button.addEventListener('click', () => fill_search(
            button.textContent.trim()
        ))
    });
    document.querySelector('#search-bar').addEventListener('focus', () => load_log());
    document.querySelector('#search-bar').addEventListener('blur', () => {
        setTimeout(hide_log, 150)
    });

});

// Fetch and display sentiment data

async function get_data(event) {
    event.preventDefault();

    const search = document.querySelector('#search-topic');
    search.className = 'search-btn-disabled';
    search.disabled = true;
    search.textContent = 'Searching';

    const data = new FormData(event.target);

    await fetch('/sentiment', {
        method: 'POST',
        body: data,
        headers: {
            'X-CSRFToken': data.get('csrfmiddlewaretoken'),
        },
    })
    .then(response => response.json())
    .then(result => {
        if (result.error)
            alert(result.error)
        else
            load_chart(result)
    });

    search.className = 'search-btn';
    search.disabled = false;
    search.textContent = 'Search';
    document.querySelector('#search-bar').value = '';
}

// Manage search log

async function load_log() {
    const data = await get_log();
    document.querySelector('#search-bar').addEventListener('input', () => filter_log(data));
    filter_log(data);
}

async function get_log() {
    const response = await fetch('search');
    const log = await response.json();
    return log.response;
}

function filter_log(data) {
    const search = document.querySelector('#search-bar');
    const log = document.querySelector('#search-log');
    const query = search.value.toLowerCase();

    const filter = data
        .filter(result => result.includes(query))
        .slice(0, 5)
    
    log.innerHTML = '';

    if (filter.length > 0) {
        filter.forEach(result => {
            const item = document.createElement('li');
            const button = document.createElement('button');
            button.type = 'button';
            button.className = 'fill-search';
            button.textContent = result;
            item.addEventListener('click', () => fill_search(result));
            item.append(button);
            log.append(item);
        });
        log.style.display = 'block';
    } else {
        hide_log();
    }
}

function fill_search(value) {
    const search = document.querySelector('#search-bar');
    search.value = value;
    hide_log();
}

function hide_log() {
    document.querySelector('#search-log').style.display = 'none';
}
