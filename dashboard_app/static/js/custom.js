// User toggle button //
function toggleDropdown(event) {
    event.preventDefault();
    const dropdownMenu = document.getElementById('userDropdownMenu');

    if (dropdownMenu.style.display === 'none' || dropdownMenu.style.display === '') {
        dropdownMenu.style.display = 'block';
    } else {
        dropdownMenu.style.display = 'none';
    }

    window.onclick = function(event) {
        if (!event.target.matches('#userDropdown') && !event.target.matches('.dropdown-item')) {
            dropdownMenu.style.display = 'none';
          }
    };
}

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
  