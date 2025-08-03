document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  document.querySelector('#compose-form').onsubmit = send_email;

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // Specification 2 - Mailbox
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    for (let i = 0; i < emails.length; i++) {
      const email = document.createElement('div');
      email.className = `view border border-dark p-2 ${emails[i].read ? 'bg-light' : 'bg-white'}`;
      email.style.cursor = 'pointer';
      email.innerHTML = `
        <div class="d-flex justify-content-between">
          <span><b>${emails[i].sender}</b> ${emails[i].subject}</span>
          <span class="ms-auto text-muted">${emails[i].timestamp}</span>
        </div>
      `;
      email.addEventListener('click', () => view_email(emails[i].id, mailbox))
      document.querySelector('#emails-view').append(email);
    }
  });
}

// Specification 1 - Send Mail
function send_email(event) {

  event.preventDefault();
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
      recipients: document.querySelector('#compose-recipients').value,
      subject: document.querySelector('#compose-subject').value,
      body: document.querySelector('#compose-body').value,
    })
  })
  .then(response => response.json())
  .then(result => {
    if (result.error) {
      alert(result.error);
    } else {
      load_mailbox('sent');
    }
  });
}

// Specification 3 - View Email
function view_email(id, mailbox) {

  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#email-view').innerHTML = '';
  document.querySelector('#compose-view').style.display = 'none';

  document.querySelector('#email-view').style.display = 'block';

  fetch(`/emails/${id}`)
    .then(response => response.json())
    .then(email => {
      if (!email.read) {
        fetch(`/emails/${id}`, {
          method: 'PUT',
            body: JSON.stringify({
            read: true
          })
        });
      }
      const view = document.createElement('div');

      view.innerHTML = `
        <div><b>From:</b> ${email.sender}</div>
        <div><b>To:</b> ${email.recipients}</div>
        <div><b>Subject:</b> ${email.subject}</div>
        <div><b>Timestamp:</b> ${email.timestamp}</div>
        <button class="btn btn-sm btn-outline-primary" id="reply">Reply</button>
        <hr>
        <span>${email.body}</span>
        <hr>
      `;

      if (mailbox !== 'sent') {
        const archive = document.createElement('div');
        archive.innerHTML = `
          <button class="btn btn-sm btn-outline-primary">
            ${email.archived ? "Unarchive" : "Archive"}
          </button>
        `;
        archive.addEventListener('click', () => archive_email(id));
        view.append(archive);
      }

      document.querySelector('#email-view').append(view);
      document.querySelector('#reply').addEventListener('click', () => reply_email(id));
    }
  );
}

// Specification 4 - Archive, Unarchive
function archive_email(id) {
  fetch(`/emails/${id}`)
    .then(response => response.json())
    .then(email => {
      fetch(`/emails/${id}`, {
        method: 'PUT',
        body: JSON.stringify({
          archived: !email.archived
        })
      })
      .then (() => {
        load_mailbox('inbox');
      })
    }
  );
}

// Specification 5 - Reply
function reply_email(id) {
  fetch(`/emails/${id}`)
    .then(response => response.json())
    .then(email => {
      compose_email();
      document.querySelector('#compose-recipients').value = email.sender;
      if (!email.subject.startsWith("Re: ")) {
        document.querySelector('#compose-subject').value = `Re: ${email.subject}`;
      } else {
        document.querySelector('#compose-subject').value = `${email.subject}`;
      }
      document.querySelector('#compose-body').value = `On ${email.timestamp} ${email.sender} wrote:\n${email.body}\n<br>\n`;
    }
  );
}