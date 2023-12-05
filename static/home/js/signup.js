function valdatePassword(event) {
  let password1 = $('#password1Input');
  let password2 = $('#password2Input');
  if (password1.val() !== password2.val()) {
    event.preventDefault();
    giveAlert('alert', 'danger', 'Password And Confirm Password Must Be Same');
    return false;
  }
  return true;
}
(() => {
  'use strict'
  const forms = document.querySelectorAll('.needs-validation')
  // Loop over them and prevent submission
  Array.from(forms).forEach(form => {
    form.addEventListener('submit', event => {
      if (!valdatePassword(event) && !form.checkValidity()) {
        event.preventDefault()
        event.stopPropagation()
      }
      form.classList.add('was-validated')
    }, false)
  })
})()