// Fade out notification //
document.addEventListener("DOMContentLoaded", function() {
    const alerts = document.querySelectorAll('.alert');
  
    alerts.forEach((alert) => {
      setTimeout(() => {
        alert.classList.add('hide');
        setTimeout(() => {
          alert.remove();
        }, 500);
      }, 3000);
    });
  });
  