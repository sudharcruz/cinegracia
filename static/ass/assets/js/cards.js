// Add event listener to movie cards for click events
const movieCards = document.querySelectorAll('.movie_card');
movieCards.forEach(card => {
  card.addEventListener('click', function(event) {
    event.stopPropagation();
    movieCards.forEach(card => card.classList.remove('active'));
    this.classList.add('active');
  });
});

var swiper = new swiper('.swiper-container', {
  slidesPerView: 1, // Display only one slide at a time
  spaceBetween: 20,
  navigation: {
    nextEl: '.swiper-button-next',
    prevE1: '.swiper-button-prev',
  },
  keyboard: {
    enabled: true,
    onlyInViewport: false, 
  },
  noSwiping: true,
});


var swiper = new Swiper('.swiper-container', {
  slidesPerView: 'auto',
  spaceBetween: 20,
  navigation: {
    nextEl: '.swiper-button-next',
    prevEl: '.swiper-button-prev',
  },
  pagination: {
    el: '.swiper-pagination',
    clickable: true,
  },
});

document.addEventListener('DOMContentLoaded', function() {
  const popupMessage = document.getElementById('popup-message');
  const messages = document.getElementsByClassName('messages')[0];

  if (messages) {
    const errorMessages = messages.getElementsByClassName('error');
    if (errorMessages.length > 0) {
      popupMessage.innerText = errorMessages[0].innerText;
      popupMessage.classList.add('show');

      setTimeout(function() {
        popupMessage.classList.remove('show');
      }, 3000);
    }
  }
});
