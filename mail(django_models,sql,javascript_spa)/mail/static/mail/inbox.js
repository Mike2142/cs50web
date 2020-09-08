document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  document.querySelector('#compose-form').addEventListener('submit', send_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {
  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#details-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function send_email() {
  let recipients = document.querySelector('#compose-recipients').value;
  let subject = document.querySelector('#compose-subject').value;
  let body = document.querySelector('#compose-body').value;

  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
        recipients: recipients,
        subject: subject,
        body: body,
    })
  })
  .then(response => response.json())
  .then(result => {
      // Print result
      console.log(result);
      load_mailbox('sent');
  });

  event.preventDefault();
  return false
}

function load_mailbox(mailbox) {  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#details-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  let emailsView = document.querySelector('#emails-view');
  emailsView.innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // load emails via HTTP API  
  fetch('/emails/' + mailbox )
  .then(response => response.json())
  .then(emails => {

    emails.forEach(email => {
      let domElement = document.createElement("DIV");
      domElement.setAttribute('id', 'email'+ email.id);
      domElement.innerHTML = email.sender + ' / ' + email.subject + ' / ' + email.timestamp;
      if (!email.read) { domElement.style.color = 'green'}
      emailsView.append(domElement);
      document.querySelector(`#email${email.id}`).addEventListener('click', () => open_mail(email.id));
    });
  });
}

function open_mail(emailId) {

  fetch(`/emails/${emailId}`)
  .then(response => response.json())
  .then(email => {
    if (!email.read) {read_email(emailId)};
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#details-view').style.display = 'block';
    document.querySelector('#compose-view').style.display = 'none';

    document.querySelector('#details-sender').innerHTML = 'from: ' + email.sender;
    document.querySelector('#details-recipients').innerHTML = 'to: ' + [...email.recipients];
    document.querySelector('#details-timestamp').innerHTML = 'time: ' + email.timestamp;
    document.querySelector('#details-subject').innerHTML = 'subject: ' + email.subject;
    document.querySelector('#details-body').innerHTML = 'body: ' + email.body;

    let detailsView = document.querySelector('#details-view');
    let currentUser = document.querySelector('#user-email').innerHTML;
    detailsView.querySelectorAll('BUTTON').forEach( button => button.remove() );

    let archiveButton = document.createElement('BUTTON');
    if (!email.archived) {
      archiveButton.addEventListener('click', () => archive_email(emailId));
      archiveButton.innerHTML = 'archive';
    } else {
      archiveButton.addEventListener('click', () => unarchive_email(emailId));
      archiveButton.innerHTML = 'unarchive';
    }

    if (currentUser != email.sender) {
      detailsView.append(archiveButton)
    }

    let replyButton = document.createElement('BUTTON');
    replyButton.innerHTML = 'reply'
    detailsView.append(replyButton)
    replyButton.addEventListener('click', () => reply_email(emailId));
  });
}

function read_email(emailId) {

  fetch(`/emails/${emailId}`, {
    method: 'PUT',
    body: JSON.stringify({
      read: true
    })
  });
}

function archive_email(emailId) {

  fetch(`/emails/${emailId}`, {
    method: 'PUT',
    body: JSON.stringify({
      archived: true
    })
  }).then( () => load_mailbox('inbox'));
}

function unarchive_email(emailId) {

  fetch(`/emails/${emailId}`, {
    method: 'PUT',
    body: JSON.stringify({
      archived: false
    })
  }).then( () => load_mailbox('inbox'));

}

function reply_email(emailId) {
  compose_email();

  let currentUser = document.querySelector('#user-email').innerHTML;

  //prefill
  fetch(`/emails/${emailId}`)
  .then(response => response.json())
  .then(email => {
    if (currentUser == email.sender) {
      document.querySelector('#compose-recipients').value = [...email.recipients];
    } else {
      document.querySelector('#compose-recipients').value = email.sender;
    }
    document.querySelector('#compose-subject').value = 'Re: ' + email.subject;
    document.querySelector('#compose-body').value = `\n\n------\nOn ${email.timestamp} ${email.sender} wrote:\n${email.body}`;
    });
}



